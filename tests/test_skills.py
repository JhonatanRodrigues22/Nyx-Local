import psutil
import pytest

from nyx_local.domain.processes import ProcessInfo
from nyx_local.domain.skills import (
    JsonValue,
    Skill,
    SkillDescriptor,
    SkillRegistry,
    SkillResult,
)
from nyx_local.infrastructure.process_provider import PsutilProcessProvider
from nyx_local.services.skill_service import SkillService
from nyx_local.skills import ComputerProcessListSkill, LocalEchoSkill


class FakeProcessProvider:
    def __init__(self, processes: list[ProcessInfo]) -> None:
        self._processes = processes

    def list_processes(self) -> list[ProcessInfo]:
        return self._processes


class FakePsutilProcess:
    def __init__(self, info: dict[str, object] | Exception) -> None:
        self._info = info

    @property
    def info(self) -> dict[str, object]:
        if isinstance(self._info, Exception):
            raise self._info
        return self._info


class ExplodingSkill(Skill):
    @property
    def descriptor(self) -> SkillDescriptor:
        return SkillDescriptor(
            id="local.exploding",
            name="Exploding",
            description="Raises for executor validation.",
            version="0.1.0",
        )

    def execute(self, input_value: JsonValue) -> SkillResult:
        del input_value
        raise RuntimeError("internal detail must not escape")


class InvalidPrefixSkill(ExplodingSkill):
    @property
    def descriptor(self) -> SkillDescriptor:
        return SkillDescriptor(
            id="system.invalid",
            name="Invalid",
            description="Uses a disallowed prefix.",
            version="0.1.0",
        )


def test_skill_registry_registers_and_lists_descriptors() -> None:
    registry = SkillRegistry()
    skill = LocalEchoSkill()

    registry.register(skill)

    assert registry.get("local.echo") is skill
    assert registry.list_descriptors() == [skill.descriptor]


def test_skill_registry_rejects_duplicate_id() -> None:
    registry = SkillRegistry()
    registry.register(LocalEchoSkill())

    with pytest.raises(ValueError, match="already registered"):
        registry.register(LocalEchoSkill())


def test_skill_registry_rejects_disallowed_prefix() -> None:
    registry = SkillRegistry()

    with pytest.raises(ValueError, match="local. or computer"):
        registry.register(InvalidPrefixSkill())


def test_local_echo_returns_message() -> None:
    result = LocalEchoSkill().execute({"message": "hello"})

    assert result.success is True
    assert result.result == {"message": "hello"}
    assert result.error is None


@pytest.mark.parametrize("input_value", [None, {}, {"message": 42}, "hello"])
def test_local_echo_rejects_invalid_input(input_value: JsonValue) -> None:
    result = LocalEchoSkill().execute(input_value)

    assert result.success is False
    assert result.error is not None
    assert result.error.code == "INVALID_SKILL_INPUT"


def test_computer_process_list_returns_safe_contract_fields_only() -> None:
    skill = ComputerProcessListSkill(
        FakeProcessProvider(
            [
                ProcessInfo(pid=42, name="Code.exe", status="running"),
                ProcessInfo(pid=7, name="python.exe", status="sleeping"),
            ]
        )
    )

    result = skill.execute({})

    assert result.success is True
    assert result.result == {
        "processes": [
            {"pid": 42, "name": "Code.exe", "status": "running"},
            {"pid": 7, "name": "python.exe", "status": "sleeping"},
        ],
        "count": 2,
        "limit": 200,
        "truncated": False,
    }
    assert isinstance(result.result, dict)
    for process in result.result["processes"]:
        assert set(process) == {"pid", "name", "status"}
        assert "cmdline" not in process
        assert "cwd" not in process
        assert "environ" not in process
        assert "exe" not in process


def test_computer_process_list_applies_default_limit() -> None:
    result = ComputerProcessListSkill(FakeProcessProvider([])).execute({})

    assert result.success is True
    assert isinstance(result.result, dict)
    assert result.result["limit"] == 200


def test_computer_process_list_respects_limit_and_truncated_flag() -> None:
    skill = ComputerProcessListSkill(
        FakeProcessProvider(
            [
                ProcessInfo(pid=1, name="a.exe", status="running"),
                ProcessInfo(pid=2, name="b.exe", status="running"),
                ProcessInfo(pid=3, name="c.exe", status="running"),
            ]
        )
    )

    result = skill.execute({"limit": 2})

    assert result.success is True
    assert isinstance(result.result, dict)
    assert result.result["count"] == 2
    assert result.result["limit"] == 2
    assert result.result["truncated"] is True
    assert result.result["processes"] == [
        {"pid": 1, "name": "a.exe", "status": "running"},
        {"pid": 2, "name": "b.exe", "status": "running"},
    ]


def test_computer_process_list_caps_limit_above_maximum() -> None:
    result = ComputerProcessListSkill(FakeProcessProvider([])).execute({"limit": 999})

    assert result.success is True
    assert isinstance(result.result, dict)
    assert result.result["limit"] == 200


@pytest.mark.parametrize(
    "input_value",
    ["bad", {"limit": 0}, {"limit": -1}, {"limit": "10"}, {"limit": True}],
)
def test_computer_process_list_rejects_invalid_input(input_value: JsonValue) -> None:
    result = ComputerProcessListSkill(FakeProcessProvider([])).execute(input_value)

    assert result.success is False
    assert result.error is not None
    assert result.error.code == "INVALID_SKILL_INPUT"


def test_psutil_process_provider_omits_inaccessible_processes(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def process_iter(attrs: list[str]) -> list[FakePsutilProcess]:
        assert attrs == ["pid", "name", "status"]
        return [
            FakePsutilProcess({"pid": 2, "name": "visible.exe", "status": "running"}),
            FakePsutilProcess(psutil.AccessDenied(pid=3, name="hidden.exe")),
            FakePsutilProcess({"pid": 1, "name": "first.exe", "status": "sleeping"}),
        ]

    monkeypatch.setattr(psutil, "process_iter", process_iter)

    assert PsutilProcessProvider().list_processes() == [
        ProcessInfo(pid=1, name="first.exe", status="sleeping"),
        ProcessInfo(pid=2, name="visible.exe", status="running"),
    ]


def test_skill_service_converts_exception_to_structured_error() -> None:
    registry = SkillRegistry()
    registry.register(ExplodingSkill())
    service = SkillService(registry)

    result = service.execute("local.exploding", {})

    assert result.success is False
    assert result.error is not None
    assert result.error.code == "REMOTE_COMMAND_FAILED"
    assert "internal detail" not in result.error.message


def test_skill_service_returns_structured_not_found_error() -> None:
    result = SkillService(SkillRegistry()).execute("local.missing", {})

    assert result.success is False
    assert result.error is not None
    assert result.error.code == "SKILL_NOT_FOUND"
