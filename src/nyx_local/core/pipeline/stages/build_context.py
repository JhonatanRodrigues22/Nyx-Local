from __future__ import annotations

from nyx_local.core.pipeline.interfaces import Stage
from nyx_local.core.pipeline.models import PipelineContext


class BuildContextStage(Stage):
    """Build the initial structured context for reasoning."""

    id = "build_context"
    name = "Build Context"
    priority = 30
    enabled = True

    def execute(self, context: PipelineContext) -> PipelineContext:
        context.current_context.update(
            {
                "message": context.normalized_message,
                "intent": context.detected_intent,
                "source": context.metadata.get("source", "unknown"),
            }
        )
        context.add_log("Context built.")
        return context
