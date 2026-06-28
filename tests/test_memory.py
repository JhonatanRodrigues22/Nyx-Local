from pathlib import Path

from nyx_local.infrastructure import JsonMemoryProvider
from nyx_local.services import MemoryService


def test_memory_service_creates_and_reads_memory(tmp_path: Path) -> None:
    memory = MemoryService(JsonMemoryProvider(tmp_path / "memory.json"))

    memory.set("user", "JJ")

    assert memory.get("user") == "JJ"
    assert memory.exists("user") is True


def test_memory_service_updates_existing_memory(tmp_path: Path) -> None:
    memory = MemoryService(JsonMemoryProvider(tmp_path / "memory.json"))

    first_entry = memory.set("favorite_language", "Python")
    updated_entry = memory.set("favorite_language", "Python 3.13+")

    assert memory.get("favorite_language") == "Python 3.13+"
    assert updated_entry.created_at == first_entry.created_at
    assert updated_entry.updated_at >= first_entry.updated_at


def test_memory_service_deletes_memory(tmp_path: Path) -> None:
    memory = MemoryService(JsonMemoryProvider(tmp_path / "memory.json"))
    memory.set("user", "JJ")

    deleted = memory.delete("user")

    assert deleted is True
    assert memory.exists("user") is False
    assert memory.get("user") is None


def test_memory_service_persists_between_provider_instances(tmp_path: Path) -> None:
    memory_path = tmp_path / "memory.json"
    first_memory = MemoryService(JsonMemoryProvider(memory_path))

    first_memory.set("user", "JJ")
    first_memory.set("favorite_language", "Python")

    second_memory = MemoryService(JsonMemoryProvider(memory_path))

    assert second_memory.get("user") == "JJ"
    assert second_memory.get("favorite_language") == "Python"
