from __future__ import annotations

from nyx_local.core.pipeline.interfaces import Stage
from nyx_local.core.pipeline.models import PipelineContext


class NormalizeStage(Stage):
    """Normalize user input for downstream reasoning stages."""

    id = "normalize"
    name = "Normalize"
    priority = 10
    enabled = True

    def execute(self, context: PipelineContext) -> PipelineContext:
        context.normalized_message = " ".join(context.original_message.strip().split())
        context.add_log("Input normalized.")
        return context
