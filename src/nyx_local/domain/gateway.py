from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from nyx_local.domain.skills import JsonValue, SkillDescriptor, SkillResult

PROTOCOL_VERSION = "1.0"


class ConnectionState(StrEnum):
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    HANDSHAKING = "handshaking"
    CONNECTED = "connected"
    RECONNECTING = "reconnecting"
    STOPPED = "stopped"


class ProtocolValidationError(ValueError):
    """Raised when a wire envelope does not match protocol 1.0."""


@dataclass(slots=True, frozen=True)
class LocalHandshake:
    token: str = field(repr=False)
    instance_id: str
    platform: str
    version: str
    protocol_version: str = PROTOCOL_VERSION

    def to_wire(self) -> dict[str, JsonValue]:
        return {
            "type": "local.handshake",
            "protocolVersion": self.protocol_version,
            "token": self.token,
            "instanceId": self.instance_id,
            "platform": self.platform,
            "version": self.version,
        }


@dataclass(slots=True, frozen=True)
class LocalHandshakeAccepted:
    instance_id: str
    protocol_version: str = PROTOCOL_VERSION

    @classmethod
    def from_wire(cls, payload: dict[str, JsonValue]) -> LocalHandshakeAccepted:
        _require_envelope(payload, "local.handshake.accepted")
        return cls(instance_id=_require_string(payload, "instanceId"))


@dataclass(slots=True, frozen=True)
class LocalCapabilityAnnouncement:
    instance_id: str
    capabilities: list[SkillDescriptor]
    protocol_version: str = PROTOCOL_VERSION

    def to_wire(self) -> dict[str, JsonValue]:
        return {
            "type": "local.capabilities.announcement",
            "protocolVersion": self.protocol_version,
            "instanceId": self.instance_id,
            "capabilities": [descriptor.to_wire() for descriptor in self.capabilities],
        }


@dataclass(slots=True, frozen=True)
class LocalCommandRequest:
    request_id: str
    instance_id: str
    capability_id: str
    input_value: JsonValue = None
    protocol_version: str = PROTOCOL_VERSION

    @classmethod
    def from_wire(cls, payload: dict[str, JsonValue]) -> LocalCommandRequest:
        _require_envelope(payload, "local.command.request")
        return cls(
            request_id=_require_string(payload, "requestId"),
            instance_id=_require_string(payload, "instanceId"),
            capability_id=_require_string(payload, "capabilityId"),
            input_value=payload.get("input"),
        )


@dataclass(slots=True, frozen=True)
class ProtocolError:
    code: str
    message: str
    retryable: bool
    details: dict[str, JsonValue] = field(default_factory=dict)

    @classmethod
    def from_wire(cls, payload: dict[str, JsonValue]) -> ProtocolError:
        code = _require_string(payload, "code")
        message = _require_string(payload, "message")
        retryable = payload.get("retryable")
        if not isinstance(retryable, bool):
            raise ProtocolValidationError("error.retryable must be a boolean")
        raw_details = payload.get("details", {})
        if not isinstance(raw_details, dict) or not all(
            isinstance(key, str) for key in raw_details
        ):
            raise ProtocolValidationError("error.details must be an object")
        return cls(code=code, message=message, retryable=retryable, details=raw_details)

    def to_wire(self) -> dict[str, JsonValue]:
        payload: dict[str, JsonValue] = {
            "code": self.code,
            "message": self.message,
            "retryable": self.retryable,
        }
        if self.details:
            payload["details"] = self.details
        return payload


@dataclass(slots=True, frozen=True)
class LocalErrorEnvelope:
    error: ProtocolError
    protocol_version: str = PROTOCOL_VERSION

    @classmethod
    def from_wire(cls, payload: dict[str, JsonValue]) -> LocalErrorEnvelope:
        _require_envelope(payload, "local.error")
        raw_error = payload.get("error")
        if not isinstance(raw_error, dict):
            raise ProtocolValidationError("local.error requires an error object")
        return cls(error=ProtocolError.from_wire(raw_error))


@dataclass(slots=True, frozen=True)
class LocalCommandResult:
    request_id: str
    instance_id: str
    capability_id: str
    success: bool
    result: JsonValue = None
    error: ProtocolError | None = None
    protocol_version: str = PROTOCOL_VERSION

    @classmethod
    def from_skill_result(
        cls,
        request: LocalCommandRequest,
        skill_result: SkillResult,
    ) -> LocalCommandResult:
        error = None
        if skill_result.error is not None:
            error = ProtocolError(
                code=skill_result.error.code,
                message=skill_result.error.message,
                retryable=skill_result.error.retryable,
                details=skill_result.error.details,
            )
        return cls(
            request_id=request.request_id,
            instance_id=request.instance_id,
            capability_id=request.capability_id,
            success=skill_result.success,
            result=skill_result.result,
            error=error,
        )

    def to_wire(self) -> dict[str, JsonValue]:
        payload: dict[str, JsonValue] = {
            "type": "local.command.result",
            "protocolVersion": self.protocol_version,
            "requestId": self.request_id,
            "instanceId": self.instance_id,
            "capabilityId": self.capability_id,
            "success": self.success,
        }
        if self.success:
            payload["result"] = self.result
        elif self.error is not None:
            payload["error"] = self.error.to_wire()
        return payload


@dataclass(slots=True, frozen=True)
class LocalHeartbeat:
    instance_id: str
    sent_at: str
    protocol_version: str = PROTOCOL_VERSION

    @classmethod
    def now(cls, instance_id: str) -> LocalHeartbeat:
        return cls(instance_id=instance_id, sent_at=datetime.now(UTC).isoformat())

    def to_wire(self) -> dict[str, JsonValue]:
        return {
            "type": "local.heartbeat",
            "protocolVersion": self.protocol_version,
            "instanceId": self.instance_id,
            "sentAt": self.sent_at,
        }


class GatewayTransport(ABC):
    """Domain boundary implemented by a concrete bidirectional transport."""

    @abstractmethod
    async def connect(self) -> None:
        """Open the transport connection."""

    @abstractmethod
    async def send(self, payload: dict[str, JsonValue]) -> None:
        """Serialize and send one protocol envelope."""

    @abstractmethod
    async def receive(self) -> dict[str, JsonValue]:
        """Receive and deserialize one protocol envelope."""

    @abstractmethod
    async def close(self) -> None:
        """Close the current transport connection."""


def parse_message_type(payload: dict[str, JsonValue]) -> str:
    message_type = payload.get("type")
    if not isinstance(message_type, str):
        raise ProtocolValidationError("message.type must be a string")
    protocol_version = payload.get("protocolVersion")
    if protocol_version != PROTOCOL_VERSION:
        raise ProtocolValidationError(f"unsupported protocol version: {protocol_version}")
    return message_type


def _require_envelope(payload: dict[str, JsonValue], expected_type: str) -> None:
    message_type = parse_message_type(payload)
    if message_type != expected_type:
        raise ProtocolValidationError(f"expected {expected_type}, received {message_type}")


def _require_string(payload: dict[str, JsonValue], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value:
        raise ProtocolValidationError(f"{key} must be a non-empty string")
    return value
