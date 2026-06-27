from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Settings:
    """Application settings prepared for future configuration loading."""

    project_name: str = "Nyx Local"
    version: str = "0.1.0"
    debug: bool = False
