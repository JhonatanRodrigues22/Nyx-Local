from __future__ import annotations

from nyx_local.core.skills.exceptions import SkillNotFoundError
from nyx_local.core.skills.models import SkillRequest
from nyx_local.core.skills.models.skill_registration import SkillRegistration
from nyx_local.core.skills.registry import SkillRegistry


class SkillResolver:
    """Resolves a skill request into a registry entry."""

    def __init__(self, registry: SkillRegistry) -> None:
        self.registry = registry

    def resolve(self, request: SkillRequest) -> SkillRegistration:
        if request.skill_id is not None:
            return self._resolve_by_id(request.skill_id)

        if request.capability is not None:
            return self._resolve_by_capability(request.capability)

        raise SkillNotFoundError("Skill request must include skill_id or capability.")

    def _resolve_by_id(self, skill_id: str) -> SkillRegistration:
        if not self.registry.contains(skill_id):
            raise SkillNotFoundError(f"Skill not found: {skill_id}")

        return self.registry.get_registration(skill_id)

    def _resolve_by_capability(self, capability: str) -> SkillRegistration:
        for manifest in self.registry.manifests():
            if capability in manifest.capabilities:
                return self.registry.get_registration(manifest.id)

        raise SkillNotFoundError(f"Skill capability not found: {capability}")
