from __future__ import annotations

from nyx_local.core.skills.discovery import SkillDiscovery
from nyx_local.core.skills.exceptions import SkillRuntimeError
from nyx_local.core.skills.executor import SkillExecutor
from nyx_local.core.skills.interfaces import Skill
from nyx_local.core.skills.models import SkillContext, SkillRequest, SkillResult
from nyx_local.core.skills.registry import SkillRegistry
from nyx_local.core.skills.resolver import SkillResolver


class SkillManager:
    """Coordinates discovery, resolution, and execution of skills."""

    def __init__(
        self,
        registry: SkillRegistry,
        discovery: SkillDiscovery | None = None,
        resolver: SkillResolver | None = None,
        executor: SkillExecutor | None = None,
    ) -> None:
        self.registry = registry
        self.discovery = discovery or SkillDiscovery()
        self.resolver = resolver or SkillResolver(registry)
        self.executor = executor or SkillExecutor()

    def load(self) -> None:
        for skill_factory in self.discovery.discover():
            self.registry.register(skill_factory)

    def get(self, skill_id: str) -> Skill:
        return self.registry.create(skill_id)

    def execute(self, request: SkillRequest, context: SkillContext | None = None) -> SkillResult:
        try:
            registration = self.resolver.resolve(request)
        except SkillRuntimeError as error:
            return SkillResult(success=False, errors=[str(error)])

        return self.executor.execute(registration, request, context or SkillContext())

    def available_skill_ids(self) -> list[str]:
        return self.registry.ids()
