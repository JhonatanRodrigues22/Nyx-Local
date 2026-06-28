from __future__ import annotations

from nyx_local.core.pipeline.interfaces import Stage
from nyx_local.core.pipeline.models import PipelineContext


class DetectIntentStage(Stage):
    """Detect a simple initial intent without invoking an LLM."""

    id = "detect_intent"
    name = "Detect Intent"
    priority = 20
    enabled = True

    def execute(self, context: PipelineContext) -> PipelineContext:
        message = context.normalized_message.lower()

        if not message:
            intent = "empty"
        elif message.endswith("?") or message.startswith(("what ", "why ", "how ", "when ")):
            intent = "question"
        elif message.startswith(("set ", "save ", "remember ")):
            intent = "memory_write"
        elif message.startswith(("delete ", "remove ", "forget ")):
            intent = "memory_delete"
        else:
            intent = "conversation"

        context.detected_intent = intent
        context.add_log(f"Intent detected: {intent}.")
        return context
