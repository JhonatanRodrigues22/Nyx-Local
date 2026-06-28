from __future__ import annotations

from typing import Any

from nyx_local.domain.memory import MemoryEntry, MemoryProvider


class MemoryService:
    """Application service for memory operations."""

    def __init__(self, provider: MemoryProvider) -> None:
        self.provider = provider

    def get(self, key: str) -> Any | None:
        entry = self.provider.get(key)

        if entry is None:
            return None

        return entry.value

    def get_entry(self, key: str) -> MemoryEntry | None:
        return self.provider.get(key)

    def set(self, key: str, value: Any, metadata: dict[str, Any] | None = None) -> MemoryEntry:
        return self.provider.set(key, value, metadata)

    def delete(self, key: str) -> bool:
        return self.provider.delete(key)

    def exists(self, key: str) -> bool:
        return self.provider.exists(key)
