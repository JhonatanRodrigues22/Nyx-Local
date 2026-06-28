from __future__ import annotations

from typing import Any, Protocol

from nyx_local.core.pipeline.interfaces import Stage
from nyx_local.core.pipeline.models import PipelineContext


class MemoryEntryReader(Protocol):
    def get_entry(self, key: str) -> Any | None:
        """Return a memory entry by key."""


class RetrieveMemoryStage(Stage):
    """Retrieve explicit memory keys when a memory service is available."""

    def __init__(self, memory_reader: MemoryEntryReader | None = None) -> None:
        self.memory_reader = memory_reader

    def execute(self, context: PipelineContext) -> PipelineContext:
        requested_keys = context.metadata.get("memory_keys", [])

        if self.memory_reader is None or not isinstance(requested_keys, list):
            context.add_log("Memory retrieval skipped.")
            return context

        for key in requested_keys:
            if not isinstance(key, str):
                continue

            entry = self.memory_reader.get_entry(key)

            if entry is not None:
                context.retrieved_memory[key] = entry.value

        context.add_log(f"Memory retrieved: {len(context.retrieved_memory)} item(s).")
        return context
