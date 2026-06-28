from __future__ import annotations

from abc import ABC, abstractmethod

from nyx_local.core.skills.models import SkillResult


class Skill(ABC):
    """Base contract for future executable skills."""

    id = "skill"
    name = "Skill"
    enabled = True

    @abstractmethod
    def execute(self, payload: dict[str, object] | None = None) -> SkillResult:
        """Execute the skill with an optional payload."""
