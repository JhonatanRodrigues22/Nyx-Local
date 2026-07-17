from __future__ import annotations

from nyx_local.domain.applications import (
    APPLICATION_ALLOWLIST,
    ApplicationOpenFailure,
    ApplicationProvider,
)
from nyx_local.domain.skills import (
    JsonValue,
    Skill,
    SkillDescriptor,
    SkillError,
    SkillParameter,
    SkillResult,
)


class ComputerApplicationOpenSkill(Skill):
    """Open a small hardcoded allowlist of applications by symbolic name."""

    _descriptor = SkillDescriptor(
        id="computer.application.open",
        name="Computer Application Open",
        description="Opens an allowlisted local application by symbolic name.",
        version="0.1.0",
        parameters={
            "app": SkillParameter(
                type="string",
                required=True,
                description="Allowlisted symbolic app name.",
            )
        },
        result_description="Application open result containing app and opened.",
    )

    def __init__(self, application_provider: ApplicationProvider) -> None:
        self._application_provider = application_provider

    @property
    def descriptor(self) -> SkillDescriptor:
        return self._descriptor

    def execute(self, input_value: JsonValue) -> SkillResult:
        app = self._parse_app(input_value)
        if isinstance(app, SkillError):
            return SkillResult.failed(app)

        spec = APPLICATION_ALLOWLIST.get(app)
        if spec is None:
            return SkillResult.failed(
                SkillError(
                    code="APP_NOT_ALLOWED",
                    message="Application is not in the allowlist.",
                    details={
                        "capabilityId": self.descriptor.id,
                        "app": app,
                        "opened": False,
                    },
                )
            )

        try:
            self._application_provider.open_application(spec)
        except ApplicationOpenFailure:
            return SkillResult.failed(
                SkillError(
                    code="APP_OPEN_FAILED",
                    message="Application could not be opened.",
                    details={
                        "capabilityId": self.descriptor.id,
                        "app": app,
                        "opened": False,
                    },
                )
            )

        return SkillResult.succeeded({"app": app, "opened": True})

    def _parse_app(self, input_value: JsonValue) -> str | SkillError:
        if not isinstance(input_value, dict):
            return self._invalid_input("computer.application.open input must be an object")

        raw_app = input_value.get("app")
        if not isinstance(raw_app, str) or raw_app == "":
            return self._invalid_input("computer.application.open app must be a non-empty string")

        return raw_app

    def _invalid_input(self, message: str) -> SkillError:
        return SkillError(
            code="INVALID_SKILL_INPUT",
            message=message,
            details={"capabilityId": self.descriptor.id},
        )
