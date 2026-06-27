from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class Request:
    """Unified request model for future application inputs."""

    message: str
    timestamp: datetime | None = None
    origin: str | None = None


@dataclass(slots=True)
class Response:
    """Unified response model for future application outputs."""

    success: bool
    message: str
    data: object | None = None
    metadata: dict[str, object] = field(default_factory=dict)
