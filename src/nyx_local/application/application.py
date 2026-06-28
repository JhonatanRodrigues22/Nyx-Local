from nyx_local.core.models import Request, Response
from nyx_local.services.memory_service import MemoryService


class Application:
    """First application orchestrator for Nyx Local."""

    def __init__(self, memory_service: MemoryService | None = None) -> None:
        self.memory_service = memory_service

    def handle(self, request: Request) -> Response:
        return Response(
            success=True,
            message="Request handled successfully.",
            metadata={
                "request_origin": request.origin,
                "request_timestamp": request.timestamp,
            },
        )
