from dataclasses import dataclass, field

from nyx_local.application.application import Application
from nyx_local.core.models import Request, Response


@dataclass(slots=True)
class App:
    """Application bootstrap and execution entry point."""

    application: Application = field(default_factory=Application)

    def run(self, request: Request) -> Response:
        return self.application.handle(request)
