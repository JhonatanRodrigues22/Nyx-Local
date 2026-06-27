import pytest

from nyx_local.core import Registry


def test_registry_registers_and_recovers_component() -> None:
    registry = Registry()
    component = object()

    registry.register("component", component)

    assert registry.get("component") is component


def test_registry_raises_key_error_for_missing_component() -> None:
    registry = Registry()

    with pytest.raises(KeyError):
        registry.get("missing")


def test_registry_clear_removes_components() -> None:
    registry = Registry()
    registry.register("component", object())

    registry.clear()

    with pytest.raises(KeyError):
        registry.get("component")
