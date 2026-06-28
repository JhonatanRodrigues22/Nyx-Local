from __future__ import annotations

from collections.abc import Callable

from nyx_local.core.skills.interfaces import Skill

SkillFactory = Callable[[], Skill]


class SkillRegistry:
    """Registry for future executable skills."""

    def __init__(self) -> None:
        self._factories: dict[str, SkillFactory] = {}

    def register(self, skill_factory: SkillFactory) -> None:
        skill = skill_factory()
        self._factories[skill.id] = skill_factory

    def create(self, skill_id: str) -> Skill:
        return self._factories[skill_id]()

    def ids(self) -> list[str]:
        return list(self._factories)
