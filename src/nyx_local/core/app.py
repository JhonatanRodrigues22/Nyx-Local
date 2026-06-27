from dataclasses import dataclass, field

from nyx_local.application.application import Application
from nyx_local.core.models import Request, Response
from nyx_local.core.registry import Registry
from nyx_local.core.settings import Settings
from nyx_local.interfaces import ConsoleInterface


@dataclass(slots=True)
class App:
    """Application bootstrap and execution entry point."""

    application: Application = field(default_factory=Application)
    console: ConsoleInterface = field(default_factory=ConsoleInterface)
    registry: Registry = field(default_factory=Registry)
    settings: Settings = field(default_factory=Settings)

    def run(self, request: Request) -> Response:
        response = self.application.handle(request)
        self.console.render(response)
        return response
