from __future__ import annotations

from abc import ABC, abstractmethod

from nyx_local.core.pipeline.models import PipelineContext


class Stage(ABC):
    """Common interface for all intelligence pipeline stages."""

    @abstractmethod
    def execute(self, context: PipelineContext) -> PipelineContext:
        """Run the stage and return the updated pipeline context."""
