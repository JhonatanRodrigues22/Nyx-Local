from __future__ import annotations

from nyx_local.core.skills.interfaces import Skill
from nyx_local.core.skills.registry import SkillRegistry


class SkillManager:
    """Coordinates future skill lookup without owning skill implementations."""

    def __init__(self, registry: SkillRegistry) -> None:
        self.registry = registry

    def get(self, skill_id: str) -> Skill:
        return self.registry.create(skill_id)

    def available_skill_ids(self) -> list[str]:
        return self.registry.ids()
