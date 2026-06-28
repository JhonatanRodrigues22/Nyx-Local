from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

from nyx_local.core.skills.registry import SkillFactory


class SkillDiscovery:
    """Discovers skill factories without registering or executing them."""

    def __init__(
        self,
        search_paths: Iterable[str | Path] | None = None,
        candidate_factories: Iterable[SkillFactory] | None = None,
    ) -> None:
        self.search_paths = [Path(path) for path in (search_paths or [])]
        self._candidate_factories = list(candidate_factories or [])

    def discover(self) -> list[SkillFactory]:
        """Return discovered skill factories.

        File-system and entry-point loading are future extensions. The runtime
        already keeps discovery isolated so those sources can be added here.
        """
        return list(self._candidate_factories)
