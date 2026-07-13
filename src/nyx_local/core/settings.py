import os
import re
import socket
from collections.abc import Mapping
from dataclasses import dataclass, field
from urllib.parse import urlparse


@dataclass(slots=True, frozen=True)
class MemorySettings:
    """Memory settings prepared for future provider configuration."""

    provider: str = "json"
    path: str = "data/memory.json"


def _stable_instance_id(project_name: str) -> str:
    hostname = re.sub(r"[^a-z0-9-]+", "-", socket.gethostname().lower()).strip("-")
    project = re.sub(r"[^a-z0-9-]+", "-", project_name.lower()).strip("-")
    return f"{project}-{hostname}"


@dataclass(slots=True, frozen=True)
class GatewaySettings:
    """Configuration for the resident Nyx OS gateway client."""

    url: str = "ws://127.0.0.1:4789"
    token: str | None = field(default=None, repr=False)
    instance_id: str = field(default_factory=lambda: _stable_instance_id("Nyx Local"))
    heartbeat_interval_seconds: float = 10.0
    reconnect_max_seconds: float = 30.0

    def require_token(self) -> str:
        if not self.token:
            raise ValueError("NYX_LOCAL_GATEWAY_TOKEN is required")
        return self.token


@dataclass(slots=True, frozen=True)
class Settings:
    """Application settings prepared for future configuration loading."""

    project_name: str = "Nyx Local"
    version: str = "0.1.0"
    debug: bool = False
    memory: MemorySettings = field(default_factory=MemorySettings)
    gateway: GatewaySettings = field(default_factory=GatewaySettings)

    @classmethod
    def from_env(
        cls,
        environ: Mapping[str, str] | None = None,
        *,
        require_gateway_token: bool = False,
    ) -> "Settings":
        values = os.environ if environ is None else environ
        project_name = values.get("NYX_LOCAL_PROJECT_NAME", "Nyx Local")
        token = values.get("NYX_LOCAL_GATEWAY_TOKEN") or None
        instance_id = values.get("NYX_LOCAL_INSTANCE_ID") or _stable_instance_id(project_name)
        gateway = GatewaySettings(
            url=values.get("NYX_LOCAL_GATEWAY_URL", "ws://127.0.0.1:4789"),
            token=token,
            instance_id=instance_id,
            heartbeat_interval_seconds=_positive_float(
                values,
                "NYX_LOCAL_HEARTBEAT_INTERVAL_SECONDS",
                10.0,
            ),
            reconnect_max_seconds=_positive_float(
                values,
                "NYX_LOCAL_RECONNECT_MAX_SECONDS",
                30.0,
            ),
        )
        _validate_gateway_url(gateway.url)
        if require_gateway_token:
            gateway.require_token()
        return cls(project_name=project_name, gateway=gateway)


def _positive_float(values: Mapping[str, str], name: str, default: float) -> float:
    raw_value = values.get(name)
    value = default if raw_value is None else float(raw_value)
    if value <= 0:
        raise ValueError(f"{name} must be greater than zero")
    return value


def _validate_gateway_url(url: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme != "ws" or parsed.hostname not in {"127.0.0.1", "localhost", "::1"}:
        raise ValueError("NYX_LOCAL_GATEWAY_URL must use ws:// on a loopback host")
