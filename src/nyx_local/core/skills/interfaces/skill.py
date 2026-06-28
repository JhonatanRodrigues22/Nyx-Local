from __future__ import annotations

from abc import ABC, abstractmethod

from nyx_local.core.skills.models import SkillContext, SkillManifest, SkillResult


class Skill(ABC):
    """Base contract for executable skills."""

    id = "skill"
    name = "Skill"
    description = ""
    version = "0.1.0"
    author = ""
    entrypoint = ""
    permissions: list[str] = []
    capabilities: list[str] = []
    api_version = "1"
    enabled = True

    @property
    def manifest(self) -> SkillManifest:
        """Return manifest metadata derived from the skill class."""
        return SkillManifest(
            id=self.id,
            name=self.name,
            version=self.version,
            description=self.description,
            author=self.author,
            entrypoint=self.entrypoint,
            permissions=list(self.permissions),
            capabilities=list(self.capabilities),
            api_version=self.api_version,
            enabled=self.enabled,
        )

    def on_load(self, context: SkillContext) -> None:
        """Hook called before execution starts."""
        return None

    @abstractmethod
    def execute(
        self,
        context: SkillContext,
        payload: dict[str, object] | None = None,
    ) -> SkillResult:
        """Execute the skill with injected context and optional payload."""

    def on_finish(self, context: SkillContext, result: SkillResult) -> None:
        """Hook called after execution finishes."""
        return None

    def dispose(self, context: SkillContext) -> None:
        """Hook called when runtime resources can be released."""
        return None
