from __future__ import annotations

from nyx_local.application.application import Application
from nyx_local.core.app import App
from nyx_local.core.pipeline import PipelineBuilder
from nyx_local.core.registry import Registry
from nyx_local.core.settings import Settings
from nyx_local.core.skills import (
    SkillDiscovery,
    SkillExecutor,
    SkillLifecycle,
    SkillManager,
    SkillRegistry,
    SkillResolver,
)
from nyx_local.infrastructure.memory_json import JsonMemoryProvider
from nyx_local.interfaces import ConsoleInterface
from nyx_local.services.memory_service import MemoryService


class Bootstrap:
    """Initialize and shut down the Nyx Local application components."""

    def __init__(self) -> None:
        self.settings: Settings | None = None
        self.registry: Registry | None = None
        self.app: App | None = None

    def initialize(self) -> App:
        settings = Settings()
        registry = Registry()
        memory_provider = JsonMemoryProvider(settings.memory.path)
        memory_service = MemoryService(memory_provider)
        pipeline_builder = PipelineBuilder.default(memory_reader=memory_service)
        intelligence_pipeline = pipeline_builder.build()
        skill_discovery = SkillDiscovery(search_paths=settings.skills.search_paths)
        skill_registry = SkillRegistry()
        skill_resolver = SkillResolver(registry=skill_registry)
        skill_lifecycle = SkillLifecycle()
        skill_executor = SkillExecutor(lifecycle=skill_lifecycle)
        skill_manager = SkillManager(
            registry=skill_registry,
            discovery=skill_discovery,
            resolver=skill_resolver,
            executor=skill_executor,
        )
        skill_manager.load()
        application = Application(
            memory_service=memory_service,
            intelligence_pipeline=intelligence_pipeline,
        )
        console = ConsoleInterface()

        app = App(
            application=application,
            console=console,
            registry=registry,
            settings=settings,
        )

        registry.register("settings", settings)
        registry.register("memory_provider", memory_provider)
        registry.register("memory_service", memory_service)
        registry.register("pipeline_builder", pipeline_builder)
        registry.register("intelligence_pipeline", intelligence_pipeline)
        registry.register("skill_discovery", skill_discovery)
        registry.register("skill_registry", skill_registry)
        registry.register("skill_resolver", skill_resolver)
        registry.register("skill_lifecycle", skill_lifecycle)
        registry.register("skill_executor", skill_executor)
        registry.register("skill_manager", skill_manager)
        registry.register("application", application)
        registry.register("console", console)
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
