from __future__ import annotations

from collections.abc import Callable

from nyx_local.core.pipeline.interfaces import Stage

StageFactory = Callable[[], Stage]


class StageRegistry:
    """Registry for constructing enabled pipeline stages in priority order."""

    def __init__(self) -> None:
        self._factories: dict[str, StageFactory] = {}

    def register(self, stage_factory: StageFactory) -> None:
        stage = stage_factory()
        self._factories[stage.metadata.id] = stage_factory

    def create_stages(self) -> list[Stage]:
        stages = [factory() for factory in self._factories.values()]
        enabled_stages = [stage for stage in stages if stage.metadata.enabled]
        return sorted(enabled_stages, key=lambda stage: stage.metadata.priority)

    def ids(self) -> list[str]:
        return list(self._factories)
