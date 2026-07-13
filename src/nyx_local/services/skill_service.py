from nyx_local.domain.skills import JsonValue, SkillError, SkillRegistry, SkillResult


class SkillService:
    """Resolve and execute skills without leaking exceptions to transports."""

    def __init__(self, registry: SkillRegistry) -> None:
        self._registry = registry

    def execute(self, skill_id: str, input_value: JsonValue) -> SkillResult:
        try:
            skill = self._registry.get(skill_id)
        except KeyError:
            return SkillResult.failed(
                SkillError(
                    code="SKILL_NOT_FOUND",
                    message=f"Skill is not registered: {skill_id}",
                    details={"capabilityId": skill_id},
                )
            )

        try:
            return skill.execute(input_value)
        except Exception:
            return SkillResult.failed(
                SkillError(
                    code="REMOTE_COMMAND_FAILED",
                    message="Local skill execution failed",
                    details={"capabilityId": skill_id},
                )
            )
