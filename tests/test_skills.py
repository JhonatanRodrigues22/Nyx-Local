import pytest

from nyx_local.domain.skills import (
    JsonValue,
    Skill,
    SkillDescriptor,
    SkillRegistry,
    SkillResult,
)
from nyx_local.services.skill_service import SkillService
from nyx_local.skills import LocalEchoSkill


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
