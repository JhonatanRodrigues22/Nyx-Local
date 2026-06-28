from nyx_local.core.pipeline import IntelligencePipeline, PipelineBuilder, StageRegistry
from nyx_local.core.pipeline.interfaces import Stage
from nyx_local.core.pipeline.models import PipelineContext
from nyx_local.core.pipeline.stages import (
    ComposePromptStage,
    DetectIntentStage,
    NormalizeStage,
    ResponseValidatorStage,
    RetrieveMemoryStage,
)
from nyx_local.infrastructure import JsonMemoryProvider
from nyx_local.services import MemoryService


class MarkerStage(Stage):
    def __init__(self, marker: str) -> None:
        self.marker = marker

    def execute(self, context: PipelineContext) -> PipelineContext:
        context.logs.append(self.marker)
        return context


def test_pipeline_executes_configured_stages_in_order() -> None:
    pipeline = IntelligencePipeline(stages=[MarkerStage("first"), MarkerStage("second")])

    result = pipeline.run("hello")

    assert result.logs == ["first", "second"]
    assert result.metrics["stage_count"] == 2


def test_pipeline_normalizes_detects_intent_and_composes_prompt() -> None:
    pipeline = IntelligencePipeline(
        stages=[
            NormalizeStage(),
            DetectIntentStage(),
            ComposePromptStage(),
            ResponseValidatorStage(),
        ]
    )

    result = pipeline.run("  How   are you?  ")

    assert result.response == "Intelligence pipeline completed without LLM execution."
    assert result.internal["intent"] == "question"
    assert "User message: How are you?" in result.internal["prompt"]
    assert result.errors == []


def test_pipeline_retrieves_memory_from_explicit_metadata_keys(tmp_path) -> None:  # type: ignore[no-untyped-def]
    memory = MemoryService(JsonMemoryProvider(tmp_path / "memory.json"))
    memory.set("user", "JJ")
    pipeline = IntelligencePipeline(
        stages=[
            NormalizeStage(),
            RetrieveMemoryStage(memory_reader=memory),
            ComposePromptStage(),
            ResponseValidatorStage(),
        ]
    )

    result = pipeline.run("remember me", metadata={"memory_keys": ["user"]})

    assert result.internal["memory_keys"] == ["user"]
    assert "- user: JJ" in result.internal["prompt"]


def test_stage_registry_orders_enabled_stages_by_priority() -> None:
    registry = StageRegistry()
    registry.register(ResponseValidatorStage)
    registry.register(NormalizeStage)

    stages = registry.create_stages()

    assert [stage.metadata.id for stage in stages] == ["normalize", "validate_response"]


def test_pipeline_builder_creates_default_pipeline_with_ordered_stages() -> None:
    pipeline = PipelineBuilder.default().build()

    assert [stage.metadata.id for stage in pipeline.stages] == [
        "normalize",
        "detect_intent",
        "build_context",
        "retrieve_memory",
        "retrieve_projects",
        "reasoning_planner",
        "compose_prompt",
        "validate_response",
    ]
