from __future__ import annotations

from abc import ABC, abstractmethod

from nyx_local.core.pipeline.models import PipelineContext, StageMetadata


class Stage(ABC):
    """Common interface for all intelligence pipeline stages."""

    id = "stage"
    name = "Stage"
    priority = 100
    enabled = True

    @property
    def metadata(self) -> StageMetadata:
        return StageMetadata(
            id=self.id,
            name=self.name,
            priority=self.priority,
            enabled=self.enabled,
        )

    @abstractmethod
    def execute(self, context: PipelineContext) -> PipelineContext:
        """Run the stage and return the updated pipeline context."""
