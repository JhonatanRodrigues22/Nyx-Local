from dataclasses import dataclass, field


@dataclass(slots=True, frozen=True)
class SkillManifest:
    """Metadata that describes a skill before it is executed."""

    id: str
    name: str
    version: str
    description: str = ""
    author: str = ""
    entrypoint: str = ""
    permissions: list[str] = field(default_factory=list)
    capabilities: list[str] = field(default_factory=list)
    api_version: str = "1"
    enabled: bool = True
