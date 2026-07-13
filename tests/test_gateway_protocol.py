import secrets
from datetime import UTC, datetime

import pytest

from nyx_local.domain.gateway import (
    PROTOCOL_VERSION,
    LocalCommandRequest,
    LocalCommandResult,
    LocalErrorEnvelope,
    LocalHandshake,
    LocalHandshakeAccepted,
    LocalHeartbeat,
    ProtocolValidationError,
)
from nyx_local.domain.skills import SkillError, SkillResult


def test_handshake_serializes_exact_protocol_shape() -> None:
    token = secrets.token_urlsafe()
    handshake = LocalHandshake(
        token=token,
        instance_id="stable-instance",
        platform="windows",
        version="0.1.0",
    )

    assert handshake.to_wire() == {
        "type": "local.handshake",
        "protocolVersion": "1.0",
        "token": token,
        "instanceId": "stable-instance",
        "platform": "windows",
        "version": "0.1.0",
    }
    assert token not in repr(handshake)


def test_handshake_accepted_parses_protocol() -> None:
    accepted = LocalHandshakeAccepted.from_wire(
        {
            "type": "local.handshake.accepted",
            "protocolVersion": PROTOCOL_VERSION,
            "instanceId": "stable-instance",
        }
    )

    assert accepted.instance_id == "stable-instance"


def test_protocol_rejects_incompatible_version() -> None:
    with pytest.raises(ProtocolValidationError, match="unsupported protocol version"):
        LocalHandshakeAccepted.from_wire(
            {
                "type": "local.handshake.accepted",
                "protocolVersion": "0.0",
                "instanceId": "stable-instance",
            }
        )


@pytest.mark.parametrize(
    ("internal_code", "message"),
    [
        ("INVALID_SKILL_INPUT", "Structured local input error"),
        ("SKILL_NOT_FOUND", "Structured missing skill error"),
    ],
)
def test_command_result_maps_internal_error_and_preserves_correlation(
    internal_code: str,
    message: str,
) -> None:
    request = LocalCommandRequest.from_wire(
        {
            "type": "local.command.request",
            "protocolVersion": PROTOCOL_VERSION,
            "requestId": "request-1",
            "instanceId": "stable-instance",
            "capabilityId": "local.echo",
            "input": {"message": "hello"},
        }
    )
    result = LocalCommandResult.from_skill_result(
        request,
        SkillResult.failed(
            SkillError(
                code=internal_code,
                message=message,
                details={"capabilityId": "local.echo", "nested": {"private": "ignored"}},
            )
        ),
    )

    assert result.to_wire() == {
        "type": "local.command.result",
        "protocolVersion": PROTOCOL_VERSION,
        "requestId": "request-1",
        "instanceId": "stable-instance",
        "capabilityId": "local.echo",
        "success": False,
        "error": {
            "code": "REMOTE_COMMAND_FAILED",
            "message": message,
            "retryable": False,
            "details": {
                "capabilityId": "local.echo",
                "internalCode": internal_code,
            },
        },
    }


def test_protocol_error_parses_structured_error() -> None:
    envelope = LocalErrorEnvelope.from_wire(
        {
            "type": "local.error",
            "protocolVersion": PROTOCOL_VERSION,
            "error": {
                "code": "AUTHENTICATION_FAILED",
                "message": "Authentication failed",
                "retryable": False,
            },
        }
    )

    assert envelope.error.code == "AUTHENTICATION_FAILED"
    assert envelope.error.retryable is False


@pytest.mark.parametrize(
    "error",
    [
        {"code": "SKILL_NOT_FOUND", "message": "failed", "retryable": False},
        {"code": "REMOTE_COMMAND_FAILED", "message": 42, "retryable": False},
        {"code": "REMOTE_COMMAND_FAILED", "message": "failed", "retryable": "no"},
        {
            "code": "REMOTE_COMMAND_FAILED",
            "message": "failed",
            "retryable": False,
            "details": [],
        },
    ],
)
def test_protocol_error_rejects_invalid_network_fields(error: dict[str, object]) -> None:
    with pytest.raises(ProtocolValidationError):
        LocalErrorEnvelope.from_wire(
            {
                "type": "local.error",
                "protocolVersion": PROTOCOL_VERSION,
                "error": error,
            }
        )


def test_heartbeat_uses_iso_utc_timestamp() -> None:
    heartbeat = LocalHeartbeat.now("stable-instance")
    parsed = datetime.fromisoformat(heartbeat.sent_at)

    assert parsed.tzinfo == UTC
    assert heartbeat.to_wire()["protocolVersion"] == PROTOCOL_VERSION
