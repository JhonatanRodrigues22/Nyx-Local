from __future__ import annotations

from nyx_local.core.skills.interfaces import Skill
from nyx_local.core.skills.models import SkillContext, SkillResult


class SkillLifecycle:
    """Coordinates lifecycle hooks for a skill execution."""

    def load(self, skill: Skill, context: SkillContext) -> None:
        skill.on_load(context)

    def finish(self, skill: Skill, context: SkillContext, result: SkillResult) -> None:
        skill.on_finish(context, result)

    def dispose(self, skill: Skill, context: SkillContext) -> None:
        skill.dispose(context)
