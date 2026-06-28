from dataclasses import dataclass, field


@dataclass(slots=True)
class SkillRequest:
    """Request used by the skill runtime to resolve and execute a skill."""

    skill_id: str | None = None
    capability: str | None = None
    payload: dict[str, object] = field(default_factory=dict)
