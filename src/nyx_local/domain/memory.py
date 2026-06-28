from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass(slots=True)
class MemoryEntry:
    """Persistent memory entry prepared for future metadata evolution."""

    key: str
    value: Any
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    metadata: dict[str, Any] = field(default_factory=dict)


class MemoryProvider(ABC):
    """Memory persistence contract independent from infrastructure details."""

    @abstractmethod
    def get(self, key: str) -> MemoryEntry | None:
        """Return a memory entry by key."""

    @abstractmethod
    def set(self, key: str, value: Any, metadata: dict[str, Any] | None = None) -> MemoryEntry:
        """Store or update a memory entry."""

    @abstractmethod
    def delete(self, key: str) -> bool:
        """Delete a memory entry by key."""

    @abstractmethod
    def exists(self, key: str) -> bool:
        """Check if a memory entry exists."""
