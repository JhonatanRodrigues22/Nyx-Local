from __future__ import annotations

import psutil

from nyx_local.domain.processes import ProcessInfo


class PsutilProcessProvider:
    """Read process metadata through psutil without exposing sensitive fields."""

    def list_processes(self) -> list[ProcessInfo]:
        processes: list[ProcessInfo] = []

        for process in psutil.process_iter(attrs=["pid", "name", "status"]):
            try:
                info = process.info
                pid = info.get("pid")
                name = info.get("name")
                status = info.get("status")
            except (psutil.AccessDenied, psutil.NoSuchProcess, psutil.ZombieProcess):
                continue

            if not isinstance(pid, int):
                continue

            processes.append(
                ProcessInfo(
                    pid=pid,
                    name=name if isinstance(name, str) and name else "unknown",
                    status=status if isinstance(status, str) and status else "unknown",
                )
            )

        return sorted(processes, key=lambda process_info: process_info.pid)
