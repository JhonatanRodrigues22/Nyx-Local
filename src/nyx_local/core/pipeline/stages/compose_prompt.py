from __future__ import annotations

from nyx_local.core.pipeline.interfaces import Stage
from nyx_local.core.pipeline.models import PipelineContext


class ComposePromptStage(Stage):
    """Compose the future LLM prompt from pipeline context."""

    def execute(self, context: PipelineContext) -> PipelineContext:
        memory_lines = [
            f"- {key}: {value}" for key, value in sorted(context.retrieved_memory.items())
        ]
        plan_lines = [f"- {step}" for step in context.reasoning_plan]

        context.prompt = "\n".join(
            [
                "You are Nyx Local.",
                f"User message: {context.normalized_message}",
                f"Detected intent: {context.detected_intent}",
                "Retrieved memory:",
                *(memory_lines or ["- none"]),
                "Reasoning plan:",
                *plan_lines,
            ]
        )
        context.add_log("Prompt composed.")
        return context
