from dataclasses import dataclass, field


@dataclass(slots=True, frozen=True)
class MemorySettings:
    """Memory settings prepared for future provider configuration."""

    provider: str = "json"
    path: str = "data/memory.json"


@dataclass(slots=True, frozen=True)
class SkillSettings:
    """Skill runtime settings prepared for future discovery sources."""

    search_paths: tuple[str, ...] = ("skills",)
    api_version: str = "1"


@dataclass(slots=True, frozen=True)
class Settings:
    """Application settings prepared for future configuration loading."""

    project_name: str = "Nyx Local"
    version: str = "0.1.0"
    debug: bool = False
    memory: MemorySettings = field(default_factory=MemorySettings)
    skills: SkillSettings = field(default_factory=SkillSettings)
