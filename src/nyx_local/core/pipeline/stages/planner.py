from __future__ import annotations

from nyx_local.core.pipeline.interfaces import Stage
from nyx_local.core.pipeline.models import PipelineContext


class ReasoningPlannerStage(Stage):
    """Create a minimal reasoning plan for future LLM prompting."""

    def execute(self, context: PipelineContext) -> PipelineContext:
        context.reasoning_plan = [
            "Understand the normalized user message.",
            f"Respect the detected intent: {context.detected_intent}.",
            "Use retrieved context without inventing unavailable data.",
            "Prepare a clear response for the language engine.",
        ]
        context.add_log("Reasoning plan created.")
        return context
