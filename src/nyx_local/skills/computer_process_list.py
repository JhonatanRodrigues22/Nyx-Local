from __future__ import annotations

from nyx_local.domain.processes import ProcessProvider
from nyx_local.domain.skills import (
    JsonValue,
    Skill,
    SkillDescriptor,
    SkillError,
    SkillParameter,
    SkillResult,
)


class ComputerProcessListSkill(Skill):
    """Read-only skill that lists safe process summaries."""

    DEFAULT_LIMIT = 200
    MAX_LIMIT = 200

    _descriptor = SkillDescriptor(
        id="computer.process.list",
        name="Computer Process List",
        description="Lists running OS processes with safe read-only metadata.",
        version="0.1.0",
        parameters={
            "limit": SkillParameter(
                type="number",
                required=False,
                description="Maximum number of processes to return. Values above 200 are capped.",
            )
        },
        result_description=(
            "Safe process list containing pid, name, status, count, limit, and truncated."
        ),
    )

    def __init__(self, process_provider: ProcessProvider) -> None:
        self._process_provider = process_provider

    @property
    def descriptor(self) -> SkillDescriptor:
        return self._descriptor

    def execute(self, input_value: JsonValue) -> SkillResult:
        limit = self._parse_limit(input_value)
        if isinstance(limit, SkillError):
            return SkillResult.failed(limit)

        processes = self._process_provider.list_processes()
        truncated = len(processes) > limit
        limited_processes = processes[:limit]

        return SkillResult.succeeded(
            {
                "processes": [
                    {
                        "pid": process.pid,
                        "name": process.name,
                        "status": process.status,
                    }
                    for process in limited_processes
                ],
                "count": len(limited_processes),
                "limit": limit,
                "truncated": truncated,
            }
        )

    def _parse_limit(self, input_value: JsonValue) -> int | SkillError:
        if input_value is None:
            return self.DEFAULT_LIMIT

        if not isinstance(input_value, dict):
            return self._invalid_input("computer.process.list input must be an object")

        raw_limit = input_value.get("limit", self.DEFAULT_LIMIT)

        if isinstance(raw_limit, bool) or not isinstance(raw_limit, int):
            return self._invalid_input("computer.process.list limit must be an integer")

        if raw_limit <= 0:
            return self._invalid_input("computer.process.list limit must be greater than zero")

        return min(raw_limit, self.MAX_LIMIT)

    def _invalid_input(self, message: str) -> SkillError:
        return SkillError(
            code="INVALID_SKILL_INPUT",
            message=message,
            details={"capabilityId": self.descriptor.id},
        )
