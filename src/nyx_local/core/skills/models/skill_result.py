from dataclasses import dataclass, field


@dataclass(slots=True)
class SkillResult:
    """Result returned by future executable skills."""

    success: bool
    message: str
    data: object | None = None
    metadata: dict[str, object] = field(default_factory=dict)
