import asyncio
import secrets
from collections.abc import Callable

import pytest

from nyx_local.core.settings import GatewaySettings, Settings
from nyx_local.domain.gateway import GatewayTransport
from nyx_local.domain.skills import JsonValue, SkillRegistry
from nyx_local.services.gateway_service import GatewayRejectedError, GatewayService
from nyx_local.services.skill_service import SkillService
from nyx_local.skills import LocalEchoSkill


class FakeTransport(GatewayTransport):
    def __init__(
        self,
        incoming: list[dict[str, JsonValue]],
        *,
        connect_failures: int = 0,
        fail_first_heartbeat: bool = False,
    ) -> None:
        self.incoming: asyncio.Queue[dict[str, JsonValue] | Exception] = asyncio.Queue()
        for message in incoming:
            self.incoming.put_nowait(message)
        self.sent: list[dict[str, JsonValue]] = []
        self.connect_failures = connect_failures
        self.connect_count = 0
        self.connected = False
        self.fail_first_heartbeat = fail_first_heartbeat

    async def connect(self) -> None:
        self.connect_count += 1
        if self.connect_count <= self.connect_failures:
            raise ConnectionError("temporary connection failure")
        self.connected = True

    async def send(self, payload: dict[str, JsonValue]) -> None:
        if not self.connected:
            raise ConnectionError("not connected")
        if payload.get("type") == "local.heartbeat" and self.fail_first_heartbeat:
            self.fail_first_heartbeat = False
            raise ConnectionError("heartbeat send failed")
        self.sent.append(payload)

    async def receive(self) -> dict[str, JsonValue]:
        item = await self.incoming.get()
        if isinstance(item, Exception):
            raise item
        return item

    async def close(self) -> None:
        if self.connected:
            self.connected = False
            self.incoming.put_nowait(ConnectionError("closed"))


def create_service(
    transport: FakeTransport,
    *,
    heartbeat_interval: float = 10,
) -> GatewayService:
    settings = Settings(
        gateway=GatewaySettings(
            token=secrets.token_urlsafe(),
            instance_id="stable-instance",
            heartbeat_interval_seconds=heartbeat_interval,
            reconnect_max_seconds=0.01,
        )
    )
    registry = SkillRegistry()
    registry.register(LocalEchoSkill())
    return GatewayService(
        settings,
        transport,
        registry,
        SkillService(registry),
        reconnect_initial_seconds=0.001,
    )


async def wait_for(predicate: Callable[[], bool], timeout: float = 1) -> None:
    deadline = asyncio.get_running_loop().time() + timeout
    while not predicate():
        if asyncio.get_running_loop().time() >= deadline:
            raise TimeoutError("condition not met")
        await asyncio.sleep(0.001)


def test_gateway_dispatches_command_and_sends_correlated_result() -> None:
    async def scenario() -> None:
        transport = FakeTransport(
            [
                {
                    "type": "local.handshake.accepted",
                    "protocolVersion": "1.0",
                    "instanceId": "stable-instance",
                },
                {
                    "type": "local.command.request",
                    "protocolVersion": "1.0",
                    "requestId": "request-1",
                    "instanceId": "stable-instance",
                    "capabilityId": "local.echo",
                    "input": {"message": "hello"},
                },
            ]
        )
        service = create_service(transport)
        task = asyncio.create_task(service.run())
        await wait_for(
            lambda: any(message.get("type") == "local.command.result" for message in transport.sent)
        )
        await service.shutdown()
        await task

        assert [message["type"] for message in transport.sent[:2]] == [
            "local.handshake",
            "local.capabilities.announcement",
        ]
        result = next(
            message for message in transport.sent if message.get("type") == "local.command.result"
        )
        assert result["requestId"] == "request-1"
        assert result["result"] == {"message": "hello"}

    asyncio.run(scenario())


def test_gateway_sends_heartbeat_and_shuts_down_cleanly() -> None:
    async def scenario() -> None:
        transport = FakeTransport(
            [
                {
                    "type": "local.handshake.accepted",
                    "protocolVersion": "1.0",
                    "instanceId": "stable-instance",
                }
            ]
        )
        service = create_service(transport, heartbeat_interval=0.005)
        task = asyncio.create_task(service.run())
        await wait_for(
            lambda: any(message.get("type") == "local.heartbeat" for message in transport.sent)
        )
        await service.shutdown()
        await task

        heartbeats = [
            message for message in transport.sent if message.get("type") == "local.heartbeat"
        ]
        assert len(heartbeats) == 1

    asyncio.run(scenario())


def test_gateway_stops_after_non_retryable_rejection() -> None:
    async def scenario() -> None:
        transport = FakeTransport(
            [
                {
                    "type": "local.error",
                    "protocolVersion": "1.0",
                    "error": {
                        "code": "AUTHENTICATION_FAILED",
                        "message": "Authentication failed",
                        "retryable": False,
                    },
                }
            ]
        )
        service = create_service(transport)

        with pytest.raises(GatewayRejectedError, match="AUTHENTICATION_FAILED"):
            await service.run()
        assert transport.connect_count == 1

    asyncio.run(scenario())


def test_gateway_reconnects_with_backoff_after_transport_failure() -> None:
    async def scenario() -> None:
        transport = FakeTransport(
            [
                {
                    "type": "local.handshake.accepted",
                    "protocolVersion": "1.0",
                    "instanceId": "stable-instance",
                }
            ],
            connect_failures=2,
        )
        service = create_service(transport)
        task = asyncio.create_task(service.run())
        await wait_for(lambda: transport.connect_count == 3)
        await wait_for(
            lambda: any(
                message.get("type") == "local.capabilities.announcement"
                for message in transport.sent
            )
        )
        await service.shutdown()
        await task

        assert transport.connect_count == 3

    asyncio.run(scenario())


def test_gateway_reconnects_when_heartbeat_fails_without_orphaning_receive() -> None:
    async def scenario() -> None:
        transport = FakeTransport(
            [
                {
                    "type": "local.handshake.accepted",
                    "protocolVersion": "1.0",
                    "instanceId": "stable-instance",
                }
            ],
            fail_first_heartbeat=True,
        )
        service = create_service(transport, heartbeat_interval=0.005)
        task = asyncio.create_task(service.run())

        await wait_for(lambda: transport.connect_count >= 2)
        await service.shutdown()
        await asyncio.wait_for(task, timeout=0.1)

        assert task.done()
        assert service.state.value == "stopped"

    asyncio.run(scenario())
