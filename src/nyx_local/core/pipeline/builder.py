from __future__ import annotations

from typing import Any, Protocol

from nyx_local.core.pipeline.pipeline import IntelligencePipeline
from nyx_local.core.pipeline.registry import StageRegistry
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


class MemoryEntryReader(Protocol):
    def get_entry(self, key: str) -> Any | None:
        """Return a memory entry by key."""


class PipelineBuilder:
    """Builds IntelligencePipeline instances from registered stages."""

    def __init__(self, stage_registry: StageRegistry) -> None:
        self.stage_registry = stage_registry

    def build(self) -> IntelligencePipeline:
        return IntelligencePipeline(stages=self.stage_registry.create_stages())

    @classmethod
    def default(cls, memory_reader: MemoryEntryReader | None = None) -> PipelineBuilder:
        stage_registry = StageRegistry()
        stage_registry.register(NormalizeStage)
        stage_registry.register(DetectIntentStage)
        stage_registry.register(BuildContextStage)
        stage_registry.register(lambda: RetrieveMemoryStage(memory_reader=memory_reader))
        stage_registry.register(ProjectRetrievalStage)
        stage_registry.register(ReasoningPlannerStage)
        stage_registry.register(ComposePromptStage)
        stage_registry.register(ResponseValidatorStage)
        return cls(stage_registry=stage_registry)
