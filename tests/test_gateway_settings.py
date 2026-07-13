import secrets

import pytest

from nyx_local.core import Settings


def test_settings_loads_gateway_values_from_env() -> None:
    token = secrets.token_urlsafe()
    settings = Settings.from_env(
        {
            "NYX_LOCAL_GATEWAY_URL": "ws://localhost:4789",
            "NYX_LOCAL_GATEWAY_TOKEN": token,
            "NYX_LOCAL_INSTANCE_ID": "stable-test-instance",
            "NYX_LOCAL_HEARTBEAT_INTERVAL_SECONDS": "2.5",
            "NYX_LOCAL_RECONNECT_MAX_SECONDS": "8",
        },
        require_gateway_token=True,
    )

    assert settings.gateway.url == "ws://localhost:4789"
    assert settings.gateway.instance_id == "stable-test-instance"
    assert settings.gateway.heartbeat_interval_seconds == 2.5
    assert settings.gateway.reconnect_max_seconds == 8
    assert settings.gateway.require_token() == token


def test_gateway_token_is_required_for_resident_mode() -> None:
    with pytest.raises(ValueError, match="NYX_LOCAL_GATEWAY_TOKEN is required"):
        Settings.from_env({}, require_gateway_token=True)


def test_default_instance_id_is_stable() -> None:
    first = Settings.from_env({}).gateway.instance_id
    second = Settings.from_env({}).gateway.instance_id

    assert first == second
    assert first.startswith("nyx-local-")


def test_gateway_token_is_hidden_from_repr() -> None:
    token = secrets.token_urlsafe()
    settings = Settings.from_env({"NYX_LOCAL_GATEWAY_TOKEN": token})

    assert token not in repr(settings)


def test_gateway_url_rejects_non_loopback_host() -> None:
    with pytest.raises(ValueError, match="loopback"):
        Settings.from_env({"NYX_LOCAL_GATEWAY_URL": "ws://example.com:4789"})
