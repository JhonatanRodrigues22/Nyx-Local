from __future__ import annotations

import asyncio
import logging
from contextlib import suppress

from nyx_local.core.settings import Settings
from nyx_local.domain.gateway import (
    ConnectionState,
    GatewayTransport,
    LocalCapabilityAnnouncement,
    LocalCommandRequest,
    LocalCommandResult,
    LocalErrorEnvelope,
    LocalHandshake,
    LocalHandshakeAccepted,
    LocalHeartbeat,
    ProtocolValidationError,
    parse_message_type,
)
from nyx_local.domain.skills import JsonValue, SkillRegistry
from nyx_local.services.skill_service import SkillService


class GatewayRejectedError(ConnectionError):
    """Non-retryable authentication or protocol rejection from Nyx OS."""


class GatewayService:
    """Coordinate gateway transport, protocol lifecycle, and local skills."""

    def __init__(
        self,
        settings: Settings,
        transport: GatewayTransport,
        skill_registry: SkillRegistry,
        skill_service: SkillService,
        *,
        logger: logging.Logger | None = None,
        reconnect_initial_seconds: float = 1.0,
    ) -> None:
        self._settings = settings
        self._transport = transport
        self._skill_registry = skill_registry
        self._skill_service = skill_service
        self._logger = logger or logging.getLogger(__name__)
        self._reconnect_initial_seconds = reconnect_initial_seconds
        self._stop_event = asyncio.Event()
        self._handshake_completed = False
        self.state = ConnectionState.DISCONNECTED

    async def run(self) -> None:
        """Run until shutdown, reconnecting retryable transport failures with backoff."""
        self._settings.gateway.require_token()
        delay = self._reconnect_initial_seconds

        while not self._stop_event.is_set():
            self._handshake_completed = False
            try:
                await self._run_session()
            except GatewayRejectedError:
                self.state = ConnectionState.STOPPED
                raise
            except asyncio.CancelledError:
                self.state = ConnectionState.STOPPED
                raise
            except Exception as error:
                self._logger.warning(
                    "Gateway connection interrupted",
                    extra={"errorType": type(error).__name__},
                )
            finally:
                await self._transport.close()

            if self._stop_event.is_set():
                break

            if self._handshake_completed:
                delay = self._reconnect_initial_seconds
            self.state = ConnectionState.RECONNECTING
            self._logger.info("Gateway reconnect scheduled", extra={"delaySeconds": delay})
            if await self._wait_for_shutdown(delay):
                break
            delay = min(delay * 2, self._settings.gateway.reconnect_max_seconds)

        self.state = ConnectionState.STOPPED

    async def shutdown(self) -> None:
        """Stop reconnect and heartbeat activity, then close the active socket."""
        self._stop_event.set()
        await self._transport.close()

    async def _run_session(self) -> None:
        gateway = self._settings.gateway
        self.state = ConnectionState.CONNECTING
        self._logger.info("Gateway connecting")
        await self._transport.connect()

        self.state = ConnectionState.HANDSHAKING
        await self._transport.send(
            LocalHandshake(
                token=gateway.require_token(),
                instance_id=gateway.instance_id,
                platform="windows",
                version=self._settings.version,
            ).to_wire()
        )
        response = await self._transport.receive()
        message_type = parse_message_type(response)

        if message_type == "local.error":
            error = LocalErrorEnvelope.from_wire(response).error
            if not error.retryable:
                raise GatewayRejectedError(f"Gateway rejected handshake: {error.code}")
            raise ConnectionError(f"Gateway temporarily rejected handshake: {error.code}")

        accepted = LocalHandshakeAccepted.from_wire(response)
        if accepted.instance_id != gateway.instance_id:
            raise ProtocolValidationError("handshake instanceId does not match this client")

        self._handshake_completed = True
        self.state = ConnectionState.CONNECTED
        self._logger.info("Gateway handshake completed", extra={"instanceId": gateway.instance_id})
        descriptors = self._skill_registry.list_descriptors()
        await self._transport.send(
            LocalCapabilityAnnouncement(
                instance_id=gateway.instance_id,
                capabilities=descriptors,
            ).to_wire()
        )
        self._logger.info(
            "Gateway capabilities announced",
            extra={"instanceId": gateway.instance_id, "capabilityCount": len(descriptors)},
        )

        heartbeat_task = asyncio.create_task(self._heartbeat_loop())
        try:
            while not self._stop_event.is_set():
                payload = await self._transport.receive()
                await self._handle_message(payload)
        finally:
            heartbeat_task.cancel()
            with suppress(asyncio.CancelledError):
                await heartbeat_task

    async def _handle_message(self, payload: dict[str, JsonValue]) -> None:
        message_type = parse_message_type(payload)
        if message_type == "local.command.request":
            await self._handle_command(LocalCommandRequest.from_wire(payload))
            return
        if message_type == "local.error":
            error = LocalErrorEnvelope.from_wire(payload).error
            if not error.retryable:
                raise GatewayRejectedError(f"Gateway returned non-retryable error: {error.code}")
            raise ConnectionError(f"Gateway returned retryable error: {error.code}")
        raise ProtocolValidationError(f"unsupported server message: {message_type}")

    async def _handle_command(self, request: LocalCommandRequest) -> None:
        if request.instance_id != self._settings.gateway.instance_id:
            raise ProtocolValidationError("command instanceId does not match this client")

        self._logger.info(
            "Local command received",
            extra={"requestId": request.request_id, "capabilityId": request.capability_id},
        )
        skill_result = self._skill_service.execute(request.capability_id, request.input_value)
        result = LocalCommandResult.from_skill_result(request, skill_result)
        await self._transport.send(result.to_wire())
        self._logger.info(
            "Local command result sent",
            extra={
                "requestId": request.request_id,
                "capabilityId": request.capability_id,
                "success": result.success,
            },
        )

    async def _heartbeat_loop(self) -> None:
        interval = self._settings.gateway.heartbeat_interval_seconds
        while not self._stop_event.is_set():
            if await self._wait_for_shutdown(interval):
                return
            await self._transport.send(
                LocalHeartbeat.now(self._settings.gateway.instance_id).to_wire()
            )
            self._logger.debug(
                "Gateway heartbeat sent",
                extra={"instanceId": self._settings.gateway.instance_id},
            )

    async def _wait_for_shutdown(self, timeout: float) -> bool:
        try:
            await asyncio.wait_for(self._stop_event.wait(), timeout=timeout)
        except TimeoutError:
            return False
        return True
