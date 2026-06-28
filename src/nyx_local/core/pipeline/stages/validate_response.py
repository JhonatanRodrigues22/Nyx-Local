from __future__ import annotations

from nyx_local.core.pipeline.interfaces import Stage
from nyx_local.core.pipeline.models import PipelineContext


class ResponseValidatorStage(Stage):
    """Validate a future LLM response without calling an LLM."""

    def execute(self, context: PipelineContext) -> PipelineContext:
        if context.llm_response is None:
            context.validated_response = "Intelligence pipeline completed without LLM execution."
            context.add_log("Response validation skipped because no LLM response exists.")
            return context

        context.validated_response = context.llm_response.strip()
        context.add_log("Response validated.")
        return context
