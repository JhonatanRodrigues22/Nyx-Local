from dataclasses import dataclass, field


@dataclass(slots=True)
class SkillResult:
    """Standard result returned by executable skills."""

    success: bool
    data: object | None = None
    messages: list[str] = field(default_factory=list)
    artifacts: list[object] = field(default_factory=list)
    metadata: dict[str, object] = field(default_factory=dict)
    execution_time: float = 0.0
    errors: list[str] = field(default_factory=list)

    @property
    def message(self) -> str:
        """Return a compact message for older callers and console summaries."""
        return "\n".join(self.messages)
