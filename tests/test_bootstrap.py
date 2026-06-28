from nyx_local.core import Registry, Settings
from nyx_local.core.app import App
from nyx_local.core.bootstrap import Bootstrap
from nyx_local.core.pipeline import IntelligencePipeline
from nyx_local.services import MemoryService


def test_bootstrap_initializes_application_components() -> None:
    bootstrap = Bootstrap()

    app = bootstrap.initialize()

    assert isinstance(app, App)
    assert isinstance(bootstrap.settings, Settings)
    assert isinstance(bootstrap.registry, Registry)
    assert bootstrap.registry.get("app") is app
    assert bootstrap.registry.get("settings") is bootstrap.settings
    assert isinstance(bootstrap.registry.get("memory_service"), MemoryService)
    assert isinstance(bootstrap.registry.get("intelligence_pipeline"), IntelligencePipeline)
    assert app.application.memory_service is bootstrap.registry.get("memory_service")
    assert app.application.intelligence_pipeline is bootstrap.registry.get("intelligence_pipeline")


def test_bootstrap_shutdown_clears_runtime_components() -> None:
    bootstrap = Bootstrap()
    bootstrap.initialize()

    bootstrap.shutdown()

    assert bootstrap.app is None
    assert bootstrap.registry is None
    assert bootstrap.settings is None
