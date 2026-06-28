from __future__ import annotations

from collections.abc import Callable

from nyx_local.core.skills.interfaces import Skill
from nyx_local.core.skills.models import SkillManifest
from nyx_local.core.skills.models.skill_registration import SkillRegistration

SkillFactory = Callable[[], Skill]


class SkillRegistry:
    """Registry for skill metadata and factories."""

    def __init__(self) -> None:
        self._registrations: dict[str, SkillRegistration] = {}

    def register(self, skill_factory: SkillFactory) -> None:
        skill = skill_factory()
        self.register_manifest(skill.manifest, skill_factory)

    def register_manifest(self, manifest: SkillManifest, skill_factory: SkillFactory) -> None:
        self._registrations[manifest.id] = SkillRegistration(
            manifest=manifest,
            factory=skill_factory,
        )

    def create(self, skill_id: str) -> Skill:
        return self._registrations[skill_id].factory()

    def get_manifest(self, skill_id: str) -> SkillManifest:
        return self._registrations[skill_id].manifest

    def get_registration(self, skill_id: str) -> SkillRegistration:
        return self._registrations[skill_id]

    def contains(self, skill_id: str) -> bool:
        return skill_id in self._registrations

    def ids(self) -> list[str]:
        return list(self._registrations)

    def manifests(self) -> list[SkillManifest]:
        return [registration.manifest for registration in self._registrations.values()]
