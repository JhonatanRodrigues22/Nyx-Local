# Pipeline Lifecycle

This document is the official lifecycle reference for an intelligence request in Nyx Local.

## Lifecycle Diagram

```text
Application
  |
  v
IntelligencePipeline
  |
  v
Stages
  |
  v
Reasoning Planner
  |
  v
Prompt Composer
  |
  v
Future LLM
  |
  v
Response Validator
  |
  v
Future Skill Manager
  |
  v
Response
  |
  v
Future History
  |
  v
Memory
```

## Application

Application receives a `Request` and delegates reasoning preparation to the Intelligence Pipeline.

Application does not create concrete pipeline stages.

Application does not execute Skills directly.

## Pipeline

`IntelligencePipeline` runs the ordered stage list.

It does not know how stages are created.

Stage creation belongs to `PipelineBuilder` and `StageRegistry`.

## Stages

Stages update `PipelineContext`.

Each stage must:

- implement `Stage`;
- expose metadata;
- have one responsibility;
- avoid concrete execution logic.

## Planner

The Planner prepares future reasoning and execution plans.

It may later coordinate:

- planning;
- decomposition;
- multi-step reasoning;
- tool selection;
- decisions;
- Skill coordination;
- execution planning.

It must not execute actions directly.

## Prompt

Prompt Composer converts structured context into text for a future LLM.

It should only compose the prompt. It should not call a model.

## Future LLM

No LLM is currently implemented.

The future LLM will write language from prepared context.

The LLM must not own application logic.

## Validator

Response Validator validates or normalizes a future LLM response.

Without an LLM response, it returns the explicit placeholder:

```text
Intelligence pipeline completed without LLM execution.
```

## Future Skill Manager

Skill Manager will eventually select and execute Skills.

Skills answer "how to execute".

Pipeline answers "how to think".

The Skills Runtime already provides Discovery, Registry, Resolver, Executor,
Lifecycle, Context, Manifest, and standardized Result infrastructure. It does
not execute user-facing integrations yet.

## Response

Application wraps pipeline output into the project `Response` model.

The response keeps user-facing output separate from internal diagnostics.

## Future History

Conversation history is not implemented yet.

It should become a dedicated boundary instead of being embedded in stages.

## Memory

Memory currently exists through `MemoryService` and `JsonMemoryProvider`.

Pipeline memory retrieval can read explicit memory keys, but it does not own persistence behavior.

## Component Communication

```text
Bootstrap
  creates StageRegistry
  creates PipelineBuilder
  creates IntelligencePipeline
  creates SkillDiscovery
  creates SkillRegistry
  creates SkillResolver
  creates SkillLifecycle
  creates SkillExecutor
  creates SkillManager
  registers components

Application
  receives IntelligencePipeline
  runs pipeline for Request.message

Pipeline
  executes registered stages in priority order

Stages
  update PipelineContext

PipelineResult
  returns response, logs, metrics, errors, and internal diagnostics
```

## Current Architecture Review

Current state:

- unnecessary stage construction was removed from `IntelligencePipeline`;
- stage metadata prepares observability and dynamic loading;
- Skills Runtime responsibilities are separated from Pipeline responsibilities;
- Skill infrastructure exists but does not execute user-facing behavior;
- `PipelineContext` remains flat for simplicity;
- future state splitting is documented but not implemented prematurely.

Known future improvement:

- introduce dedicated state objects only when context complexity justifies it.
