from __future__ import annotations

from time import perf_counter
from typing import Any

from nyx_local.core.pipeline.interfaces import Stage
from nyx_local.core.pipeline.models import PipelineContext, PipelineResult
from nyx_local.core.pipeline.stages import (
    BuildContextStage,
    ComposePromptStage,
    DetectIntentStage,
    NormalizeStage,
    ProjectRetrievalStage,
    ReasoningPlannerStage,
    ResponseValidatorStage,
    RetrieveMemoryStage,
)


class IntelligencePipeline:
    """Runs the ordered intelligence stages before any future LLM call."""

    def __init__(self, stages: list[Stage] | None = None) -> None:
        self.stages = stages if stages is not None else self.default_stages()

    def run(self, message: str, metadata: dict[str, Any] | None = None) -> PipelineResult:
        started_at = perf_counter()
        context = PipelineContext(original_message=message, metadata=metadata or {})

        for stage in self.stages:
            try:
                context = stage.execute(context)
            except Exception as error:  # pragma: no cover - defensive boundary
                context.add_error(f"{stage.__class__.__name__}: {error}")
                break

        duration_seconds = perf_counter() - started_at

        return PipelineResult(
            response=context.validated_response,
            logs=list(context.logs),
            metrics={
                "stage_count": len(self.stages),
                "error_count": len(context.errors),
            },
            duration_seconds=duration_seconds,
            errors=list(context.errors),
            internal={
                "intent": context.detected_intent,
                "prompt": context.prompt,
                "memory_keys": list(context.retrieved_memory),
                "project_count": len(context.related_projects),
                "plan": list(context.reasoning_plan),
            },
        )

    def default_stages(self) -> list[Stage]:
        return [
            NormalizeStage(),
            DetectIntentStage(),
            BuildContextStage(),
            RetrieveMemoryStage(),
            ProjectRetrievalStage(),
            ReasoningPlannerStage(),
            ComposePromptStage(),
            ResponseValidatorStage(),
        ]
