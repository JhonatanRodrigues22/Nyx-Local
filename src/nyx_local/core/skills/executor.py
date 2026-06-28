from __future__ import annotations

from time import perf_counter

from nyx_local.core.skills.exceptions import SkillDisabledError, SkillRuntimeError
from nyx_local.core.skills.lifecycle import SkillLifecycle
from nyx_local.core.skills.models import SkillContext, SkillRequest, SkillResult
from nyx_local.core.skills.models.skill_registration import SkillRegistration


class SkillExecutor:
    """Executes resolved skills and converts failures into SkillResult."""

    def __init__(self, lifecycle: SkillLifecycle | None = None) -> None:
        self.lifecycle = lifecycle or SkillLifecycle()

    def execute(
        self,
        registration: SkillRegistration,
        request: SkillRequest,
        context: SkillContext,
    ) -> SkillResult:
        started_at = perf_counter()

        try:
            if not registration.manifest.enabled:
                raise SkillDisabledError(f"Skill is disabled: {registration.manifest.id}")

            skill = registration.factory()
            self.lifecycle.load(skill, context)
            result = skill.execute(context, request.payload)
            result.execution_time = perf_counter() - started_at
            self.lifecycle.finish(skill, context, result)
            return result
        except SkillRuntimeError as error:
            return SkillResult(
                success=False,
                errors=[str(error)],
                execution_time=perf_counter() - started_at,
                metadata={"skill_id": registration.manifest.id},
            )
        except Exception as error:
            return SkillResult(
                success=False,
                errors=[error.__class__.__name__],
                execution_time=perf_counter() - started_at,
                metadata={"skill_id": registration.manifest.id},
            )
        finally:
            if "skill" in locals():
                self.lifecycle.dispose(skill, context)
