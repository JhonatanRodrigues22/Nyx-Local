from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from nyx_local.core.skills.interfaces import Skill
from nyx_local.core.skills.models.skill_manifest import SkillManifest


@dataclass(slots=True, frozen=True)
class SkillRegistration:
    """Registry entry containing manifest metadata and a skill factory."""

    manifest: SkillManifest
    factory: Callable[[], Skill]
