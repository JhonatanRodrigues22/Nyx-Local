from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(slots=True, frozen=True)
class ProcessInfo:
    """Safe process summary exposed by read-only computer skills."""

    pid: int
    name: str
    status: str


class ProcessProvider(Protocol):
    """Read-only process source used by computer process skills."""

    def list_processes(self) -> list[ProcessInfo]:
        """Return safe process summaries without command lines or paths."""
