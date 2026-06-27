from nyx_local.core import Registry, Settings
from nyx_local.core.app import App
from nyx_local.core.bootstrap import Bootstrap


def test_bootstrap_initializes_application_components() -> None:
    bootstrap = Bootstrap()

    app = bootstrap.initialize()

    assert isinstance(app, App)
    assert isinstance(bootstrap.settings, Settings)
    assert isinstance(bootstrap.registry, Registry)
    assert bootstrap.registry.get("app") is app
    assert bootstrap.registry.get("settings") is bootstrap.settings


def test_bootstrap_shutdown_clears_runtime_components() -> None:
    bootstrap = Bootstrap()
    bootstrap.initialize()

    bootstrap.shutdown()

    assert bootstrap.app is None
    assert bootstrap.registry is None
    assert bootstrap.settings is None
