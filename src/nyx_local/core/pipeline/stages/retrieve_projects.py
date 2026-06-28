from __future__ import annotations

from nyx_local.core.pipeline.interfaces import Stage
from nyx_local.core.pipeline.models import PipelineContext


class ProjectRetrievalStage(Stage):
    """Prepare the project retrieval boundary for future integrations."""

    def execute(self, context: PipelineContext) -> PipelineContext:
        context.related_projects = []
        context.add_log("Project retrieval prepared with no project source configured.")
        return context
