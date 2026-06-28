from nyx_local.core.skills import SkillManager, SkillRegistry
from nyx_local.core.skills.interfaces import Skill
from nyx_local.core.skills.models import SkillResult


class ExampleSkill(Skill):
    id = "example"
    name = "Example"

    def execute(self, payload: dict[str, object] | None = None) -> SkillResult:
        return SkillResult(success=True, message="ok", data=payload)


def test_skill_registry_registers_and_creates_skill() -> None:
    registry = SkillRegistry()
    registry.register(ExampleSkill)

    skill = registry.create("example")

    assert isinstance(skill, ExampleSkill)
    assert registry.ids() == ["example"]


def test_skill_manager_exposes_registered_skills() -> None:
    registry = SkillRegistry()
    registry.register(ExampleSkill)
    manager = SkillManager(registry=registry)

    result = manager.get("example").execute({"value": 1})

    assert manager.available_skill_ids() == ["example"]
    assert result.success is True
    assert result.data == {"value": 1}
