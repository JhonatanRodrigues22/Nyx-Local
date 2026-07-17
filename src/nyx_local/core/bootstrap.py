from __future__ import annotations

from nyx_local.application.application import Application
from nyx_local.core.app import App
from nyx_local.core.pipeline import IntelligencePipeline
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
from nyx_local.core.registry import Registry
from nyx_local.core.settings import Settings
from nyx_local.domain.skills import SkillRegistry
from nyx_local.infrastructure.application_provider import SubprocessApplicationProvider
from nyx_local.infrastructure.memory_json import JsonMemoryProvider
from nyx_local.infrastructure.process_provider import PsutilProcessProvider
from nyx_local.infrastructure.websocket_gateway import WebSocketGateway
from nyx_local.interfaces import ConsoleInterface
from nyx_local.services.gateway_service import GatewayService
from nyx_local.services.memory_service import MemoryService
from nyx_local.services.skill_service import SkillService
from nyx_local.skills import ComputerApplicationOpenSkill, ComputerProcessListSkill, LocalEchoSkill


class Bootstrap:
    """Initialize and shut down the Nyx Local application components."""

    def __init__(self) -> None:
        self.settings: Settings | None = None
        self.registry: Registry | None = None
        self.app: App | None = None

    def initialize(self, settings: Settings | None = None) -> App:
        settings = settings or Settings()
        registry = Registry()
        memory_provider = JsonMemoryProvider(settings.memory.path)
        memory_service = MemoryService(memory_provider)
        intelligence_pipeline = IntelligencePipeline(
            stages=[
                NormalizeStage(),
                DetectIntentStage(),
                BuildContextStage(),
                RetrieveMemoryStage(memory_reader=memory_service),
                ProjectRetrievalStage(),
                ReasoningPlannerStage(),
                ComposePromptStage(),
                ResponseValidatorStage(),
            ]
        )
        application = Application(
            memory_service=memory_service,
            intelligence_pipeline=intelligence_pipeline,
        )
        console = ConsoleInterface()
        skill_registry = SkillRegistry()
        application_provider = SubprocessApplicationProvider()
        process_provider = PsutilProcessProvider()
        skill_registry.register(LocalEchoSkill())
        skill_registry.register(ComputerProcessListSkill(process_provider))
        skill_registry.register(ComputerApplicationOpenSkill(application_provider))
        skill_service = SkillService(skill_registry)
        gateway_transport = WebSocketGateway(settings.gateway.url)
        gateway_service = GatewayService(
            settings=settings,
            transport=gateway_transport,
            skill_registry=skill_registry,
            skill_service=skill_service,
        )

        app = App(
            application=application,
            console=console,
            registry=registry,
            settings=settings,
        )

        registry.register("settings", settings)
        registry.register("memory_provider", memory_provider)
        registry.register("memory_service", memory_service)
        registry.register("intelligence_pipeline", intelligence_pipeline)
        registry.register("application", application)
        registry.register("console", console)
        registry.register("application_provider", application_provider)
        registry.register("process_provider", process_provider)
        registry.register("skill_registry", skill_registry)
        registry.register("skill_service", skill_service)
        registry.register("gateway_transport", gateway_transport)
        registry.register("gateway_service", gateway_service)
        registry.register("app", app)

        self.settings = settings
        self.registry = registry
        self.app = app

        return app

    def shutdown(self) -> None:
        if self.registry is not None:
            self.registry.clear()

        self.settings = None
        self.registry = None
        self.app = None
