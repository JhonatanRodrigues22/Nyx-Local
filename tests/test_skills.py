from nyx_local.core.skills import (
    SkillDiscovery,
    SkillExecutor,
    SkillManager,
    SkillRegistry,
    SkillResolver,
)
from nyx_local.core.skills.interfaces import Skill
from nyx_local.core.skills.models import SkillContext, SkillRequest, SkillResult


class ExampleSkill(Skill):
    id = "example"
    name = "Example"
    version = "1.0.0"
    description = "Example skill for runtime tests."
    capabilities = ["example.read"]

    def execute(
        self,
        context: SkillContext,
        payload: dict[str, object] | None = None,
    ) -> SkillResult:
        return SkillResult(
            success=True,
            data={"payload": payload, "memory": context.memory},
            messages=["ok"],
        )


class LifecycleSkill(ExampleSkill):
    id = "lifecycle"
    events: list[str] = []

    def on_load(self, context: SkillContext) -> None:
        self.events.append("load")

    def execute(
        self,
        context: SkillContext,
        payload: dict[str, object] | None = None,
    ) -> SkillResult:
        self.events.append("execute")
        return SkillResult(success=True, messages=["done"])

    def on_finish(self, context: SkillContext, result: SkillResult) -> None:
        self.events.append("finish")

    def dispose(self, context: SkillContext) -> None:
        self.events.append("dispose")


def test_skill_registry_registers_manifest_and_factory() -> None:
    registry = SkillRegistry()
    registry.register(ExampleSkill)

    skill = registry.create("example")
    manifest = registry.get_manifest("example")

    assert isinstance(skill, ExampleSkill)
    assert registry.ids() == ["example"]
    assert manifest.name == "Example"
    assert manifest.version == "1.0.0"
    assert manifest.capabilities == ["example.read"]


def test_skill_manager_discovers_and_executes_registered_skills() -> None:
    discovery = SkillDiscovery(candidate_factories=[ExampleSkill])
    registry = SkillRegistry()
    manager = SkillManager(registry=registry, discovery=discovery)

    manager.load()
    result = manager.execute(
        SkillRequest(skill_id="example", payload={"value": 1}),
        SkillContext(memory="fake-memory"),
    )

    assert manager.available_skill_ids() == ["example"]
    assert result.success is True
    assert result.data == {"payload": {"value": 1}, "memory": "fake-memory"}
    assert result.messages == ["ok"]
    assert result.execution_time >= 0


def test_skill_resolver_finds_skill_by_capability() -> None:
    registry = SkillRegistry()
    registry.register(ExampleSkill)
    resolver = SkillResolver(registry)

    registration = resolver.resolve(SkillRequest(capability="example.read"))

    assert registration.manifest.id == "example"


def test_skill_executor_runs_lifecycle_hooks() -> None:
    LifecycleSkill.events = []
    registry = SkillRegistry()
    registry.register(LifecycleSkill)
    registration = registry.get_registration("lifecycle")
    executor = SkillExecutor()

    result = executor.execute(
        registration,
        SkillRequest(skill_id="lifecycle"),
        SkillContext(),
    )

    assert result.success is True
    assert LifecycleSkill.events == ["load", "execute", "finish", "dispose"]


def test_skill_manager_returns_standard_error_when_skill_is_missing() -> None:
    manager = SkillManager(registry=SkillRegistry())

    result = manager.execute(SkillRequest(skill_id="missing"))

    assert result.success is False
    assert result.errors == ["Skill not found: missing"]
