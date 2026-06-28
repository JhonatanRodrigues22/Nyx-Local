from dataclasses import dataclass, field


@dataclass(slots=True)
class SkillContext:
    """Runtime context passed to skills through dependency injection."""

    user: object | None = None
    configuration: object | None = None
    memory: object | None = None
    projects: object | None = None
    services: dict[str, object] = field(default_factory=dict)
    logger: object | None = None
    metadata: dict[str, object] = field(default_factory=dict)
    cancellation_token: object | None = None
    execution: dict[str, object] = field(default_factory=dict)
