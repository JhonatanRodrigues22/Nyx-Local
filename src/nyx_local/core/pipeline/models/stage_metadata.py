from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class StageMetadata:
    """Static metadata used to organize and observe pipeline stages."""

    id: str
    name: str
    priority: int
    enabled: bool = True
