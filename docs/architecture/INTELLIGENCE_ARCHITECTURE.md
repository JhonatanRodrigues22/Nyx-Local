# Intelligence Architecture

## Overview

The Intelligence Pipeline is the reasoning infrastructure of Nyx Local.

It prepares user input before any future LLM execution. Its purpose is to organize thinking, context, memory, project references, planning, prompt composition, and response validation behind a modular stage-based flow.

This Sprint does not implement an LLM integration. The pipeline exists so future language models can act as language engines instead of owning application logic.

## Philosophy

Nyx Local separates three responsibilities:

- Pipeline thinks.
- LLM writes.
- Skills execute.

These responsibilities must not be mixed.

The Pipeline decides how to reason about the request.

The LLM will eventually transform prepared context into language.

Skills will eventually execute concrete actions through their own managers and boundaries.

## Design Principles

- Modularity: each stage has one clear responsibility.
- Extensibility: new stages should be registered without changing pipeline execution.
- Determinism: stage order is explicit and priority-based.
- Low coupling: the pipeline executes stages but does not create them.
- High cohesion: each stage owns a narrow part of the reasoning flow.
- LLM independence: the pipeline prepares reasoning before any language model call.
- Observability: stages expose metadata and write logs into `PipelineContext`.
- Testability: stages, registries, builders, and pipeline execution can be tested independently.
- Incremental evolution: future state objects and skills can be added without rewriting the pipeline.
- Fail-safe behavior: stage errors are captured in `PipelineResult`.
- Single responsibility: Pipeline thinks, LLM writes, Skills execute.

## Full Flow

```text
User
  |
Input
  |
Normalizer
  |
Intent Detection
  |
Context Builder
  |
Memory Retrieval
  |
Project Retrieval
  |
Reasoning Planner
  |
Prompt Composer
  |
Future LLM
  |
Response Validator
  |
Response
```

## Stage Responsibilities

## Normalizer

Receives the original message and creates a normalized version. The current implementation trims whitespace and collapses repeated spacing.

## Intent Detection

Detects a simple initial intent without using an LLM. Current intents include:

- `empty`
- `question`
- `memory_write`
- `memory_delete`
- `conversation`

This is intentionally basic and exists to establish the boundary.

## Context Builder

Builds a structured context from the normalized message, detected intent, and metadata.

## Memory Retrieval

Retrieves explicit memory keys when a memory reader is available. It does not decide what to remember or execute memory writes.

## Project Retrieval

Prepares the boundary for future project sources. It currently returns no project data because no project index exists yet.

## Reasoning Planner

Creates a minimal reasoning plan for future prompting.

## Prompt Composer

Builds the final prompt that a future LLM can receive.

## Future LLM

No LLM call is implemented in this Sprint.

The future LLM must receive prepared context from the Pipeline instead of owning application logic.

## Response Validator

Validates a future LLM response. When no LLM response exists, it returns an explicit placeholder response indicating that the pipeline completed without LLM execution.

## Pipeline Context

`PipelineContext` transports state between stages.

It contains:

- original message;
- normalized message;
- detected intent;
- current context;
- retrieved memory;
- related projects;
- reasoning plan;
- final prompt;
- future LLM response;
- validated response;
- metadata;
- logs;
- errors.

The goal is to avoid passing many parameters between stages.

## Pipeline Result

`PipelineResult` is the public output of the pipeline.

It separates:

- response;
- logs;
- metrics;
- duration;
- errors;
- internal diagnostic information.

Application code can use the result without needing to inspect mutable pipeline context.

## Data Flow

Each stage receives a `PipelineContext` and returns the updated context.

```python
for stage in stages:
    context = stage.execute(context)
```

This keeps the pipeline open for extension. New intelligence can be added by introducing a new Stage and placing it in the stage list.

## Pipeline Builder and Stage Registry

`IntelligencePipeline` only executes stages.

It does not decide which stages exist, how they are ordered, or how dependencies are injected.

`StageRegistry` registers stage factories.

`PipelineBuilder` reads the registry, creates enabled stages, orders them by priority, and returns an `IntelligencePipeline`.

This prepares future dynamic configuration, plugins, debugging, and automatic stage loading.

## Stage Metadata

Every Stage exposes:

- `id`
- `name`
- `priority`
- `enabled`

These fields support future configuration, observability, monitoring, plugin loading, and debugging.

## Extensibility

## Adding a New Stage

1. Create a class that implements `Stage`.
2. Implement `execute(context) -> context`.
3. Keep the stage focused on one responsibility.
4. Add stage metadata.
5. Register the stage in `StageRegistry` through `PipelineBuilder`.
6. Add tests for ordering and behavior.
7. Document the stage when it becomes part of the official flow.

## Adding a New Skill

Skills must not be implemented directly inside the Pipeline.

Future flow:

```text
Pipeline detects intent
  |
Skill Manager selects skill
  |
Skill executes action
  |
Skill result returns to Pipeline
```

Skills answer "how to execute".

Pipeline answers "how to think".

The current Skill architecture includes `Skill`, `SkillRegistry`, `SkillManager`, and `SkillResult` as preparation only. No executable user-facing Skill is implemented yet.

## Integrating New Modules

Future integrations such as Obsidian, Home Assistant, APIs, Internet, local tools, commands, vector stores, and RAG should connect through explicit providers, services, or skill boundaries.

Do not place integration logic directly in pipeline stages.

## Architectural Decisions

## Pipeline Builder

Decision: Pipeline assembly belongs to `PipelineBuilder`, not `IntelligencePipeline`.

Reason: Pipeline execution should not be coupled to stage construction.

Advantage: Future configuration and plugin loading can change stage composition without changing pipeline execution.

Limitation: Builder configuration becomes the place where stage ordering must be reviewed carefully.

## Stage Registry

Decision: Stage construction is registered through `StageRegistry`.

Reason: This prepares automatic registration and dynamic stage loading.

Advantage: New stages can be added through registration rather than by editing pipeline execution.

Limitation: Duplicate stage ids replace earlier registrations by design.

## Stage Interface

Decision: Every stage implements the common `Stage` interface.

Reason: The pipeline can execute a simple ordered list of stages without knowing stage internals.

Advantage: Future stages can be added with low coupling.

Limitation: Stage order remains important and must be tested.

## Central Context Object

Decision: Pipeline state is transported through `PipelineContext`.

Reason: A central context prevents large method signatures and makes stage composition easier.

Advantage: Stages can add information incrementally.

Limitation: Context fields must remain disciplined to avoid becoming unstructured global state.

Future: `PipelineContext` may later split into `ConversationState`, `MemoryState`, `PlanningState`, and `ExecutionState` when those boundaries become necessary.

## Skills Boundary

Decision: Skills have their own infrastructure and must remain separate from Pipeline stages.

Reason: Pipeline decides how to think. Skills execute concrete actions.

Advantage: Future execution logic can evolve without turning the pipeline into an action layer.

## Result Object

Decision: `PipelineResult` is separate from `PipelineContext`.

Reason: Application code should receive a stable final output rather than mutable internal state.

Advantage: Internal diagnostics can evolve without changing the response boundary.

## No LLM in This Sprint

Decision: The pipeline stops before real LLM execution.

Reason: This Sprint establishes architecture before language provider integration.

Advantage: The system can evolve without giving the LLM ownership of application logic.

## Future

Possible future evolutions:

- RAG.
- multi-step planning.
- chain-of-reasoning structures.
- specialized agents.
- semantic memory.
- intelligent tools.
- response self-evaluation.
- skill manager integration.
- workflow lens integration.
- project and document retrieval.
