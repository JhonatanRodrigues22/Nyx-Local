from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class PipelineResult:
    """Final intelligence pipeline result separated from internal context."""

    response: str
    logs: list[str] = field(default_factory=list)
    metrics: dict[str, Any] = field(default_factory=dict)
    duration_seconds: float = 0.0
    errors: list[str] = field(default_factory=list)
    internal: dict[str, Any] = field(default_factory=dict)
