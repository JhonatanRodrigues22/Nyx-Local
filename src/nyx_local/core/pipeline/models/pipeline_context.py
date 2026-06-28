from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class PipelineContext:
    """Shared state transported across intelligence pipeline stages."""

    original_message: str
    normalized_message: str = ""
    detected_intent: str = "unknown"
    current_context: dict[str, Any] = field(default_factory=dict)
    retrieved_memory: dict[str, Any] = field(default_factory=dict)
    related_projects: list[dict[str, Any]] = field(default_factory=list)
    reasoning_plan: list[str] = field(default_factory=list)
    prompt: str = ""
    llm_response: str | None = None
    validated_response: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    logs: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def add_log(self, message: str) -> None:
        self.logs.append(message)

    def add_error(self, message: str) -> None:
        self.errors.append(message)
