from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from nyx_local.domain.memory import MemoryEntry, MemoryProvider


class JsonMemoryProvider(MemoryProvider):
    """JSON-backed memory provider."""

    def __init__(self, path: Path | str) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_file_exists()

    def get(self, key: str) -> MemoryEntry | None:
        data = self._load()
        raw_entry = data.get(key)

        if raw_entry is None:
            return None

        return self._entry_from_dict(key, raw_entry)

    def set(self, key: str, value: Any, metadata: dict[str, Any] | None = None) -> MemoryEntry:
        data = self._load()
        now = datetime.now(UTC)
        existing_entry = data.get(key)
        created_at = (
            self._parse_datetime(existing_entry["created_at"])
            if existing_entry is not None
            else now
        )

        entry = MemoryEntry(
            key=key,
            value=value,
            created_at=created_at,
            updated_at=now,
            metadata=metadata if metadata is not None else self._metadata_from(existing_entry),
        )

        data[key] = self._entry_to_dict(entry)
        self._save(data)

        return entry

    def delete(self, key: str) -> bool:
        data = self._load()

        if key not in data:
            return False

        del data[key]
        self._save(data)

        return True

    def exists(self, key: str) -> bool:
        return key in self._load()

    def _ensure_file_exists(self) -> None:
        if not self.path.exists():
            self._save({})

    def _load(self) -> dict[str, dict[str, Any]]:
        with self.path.open("r", encoding="utf-8") as memory_file:
            loaded = json.load(memory_file)

        if not isinstance(loaded, dict):
            return {}

        return loaded

    def _save(self, data: dict[str, dict[str, Any]]) -> None:
        with self.path.open("w", encoding="utf-8") as memory_file:
            json.dump(data, memory_file, indent=2, sort_keys=True)
            memory_file.write("\n")

    def _entry_from_dict(self, key: str, raw_entry: dict[str, Any]) -> MemoryEntry:
        return MemoryEntry(
            key=key,
            value=raw_entry.get("value"),
            created_at=self._parse_datetime(raw_entry["created_at"]),
            updated_at=self._parse_datetime(raw_entry["updated_at"]),
            metadata=dict(raw_entry.get("metadata", {})),
        )

    def _entry_to_dict(self, entry: MemoryEntry) -> dict[str, Any]:
        return {
            "value": entry.value,
            "created_at": entry.created_at.isoformat(),
            "updated_at": entry.updated_at.isoformat(),
            "metadata": entry.metadata,
        }

    def _parse_datetime(self, value: str) -> datetime:
        parsed = datetime.fromisoformat(value)

        if parsed.tzinfo is None:
            return parsed.replace(tzinfo=UTC)

        return parsed

    def _metadata_from(self, existing_entry: dict[str, Any] | None) -> dict[str, Any]:
        if existing_entry is None:
            return {}

        return dict(existing_entry.get("metadata", {}))
