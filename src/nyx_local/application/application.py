from nyx_local.core.models import Request, Response


class Application:
    """First application orchestrator for Nyx Local."""

    def handle(self, request: Request) -> Response:
        return Response(
            success=True,
            message="Request handled successfully.",
            metadata={
                "request_origin": request.origin,
                "request_timestamp": request.timestamp,
            },
        )
