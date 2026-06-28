from nyx_local.core.models import Request, Response
from nyx_local.core.pipeline import IntelligencePipeline
from nyx_local.services.memory_service import MemoryService


class Application:
    """First application orchestrator for Nyx Local."""

    def __init__(
        self,
        memory_service: MemoryService | None = None,
        intelligence_pipeline: IntelligencePipeline | None = None,
    ) -> None:
        self.memory_service = memory_service
        self.intelligence_pipeline = intelligence_pipeline

    def handle(self, request: Request) -> Response:
        pipeline_result = None

        if self.intelligence_pipeline is not None:
            pipeline_result = self.intelligence_pipeline.run(
                request.message,
                metadata={
                    "source": request.origin,
                    "request_timestamp": request.timestamp,
                },
            )

        return Response(
            success=True,
            message=(
                pipeline_result.response
                if pipeline_result is not None
                else "Request handled successfully."
            ),
            metadata={
                "request_origin": request.origin,
                "request_timestamp": request.timestamp,
                "pipeline": pipeline_result,
            },
        )
