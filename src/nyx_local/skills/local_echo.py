from nyx_local.domain.skills import (
    JsonValue,
    Skill,
    SkillDescriptor,
    SkillError,
    SkillParameter,
    SkillResult,
)


class LocalEchoSkill(Skill):
    """Technical echo used to validate the local communication round-trip."""

    _descriptor = SkillDescriptor(
        id="local.echo",
        name="Local Echo",
        description="Returns the received technical payload.",
        version="0.1.0",
        parameters={
            "message": SkillParameter(
                type="string",
                required=True,
                description="Message to echo.",
            )
        },
        result_description="Echo response.",
    )

    @property
    def descriptor(self) -> SkillDescriptor:
        return self._descriptor

    def execute(self, input_value: JsonValue) -> SkillResult:
        if not isinstance(input_value, dict) or not isinstance(input_value.get("message"), str):
            return SkillResult.failed(
                SkillError(
                    code="INVALID_SKILL_INPUT",
                    message="local.echo requires a string message",
                    details={"capabilityId": self.descriptor.id},
                )
            )

        return SkillResult.succeeded({"message": input_value["message"]})
