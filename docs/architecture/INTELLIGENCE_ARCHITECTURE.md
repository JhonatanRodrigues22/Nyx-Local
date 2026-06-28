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

## Extensibility

## Adding a New Stage

1. Create a class that implements `Stage`.
2. Implement `execute(context) -> context`.
3. Keep the stage focused on one responsibility.
4. Add the stage to the pipeline composition in Bootstrap or in tests.
5. Document the stage when it becomes part of the official flow.

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

## Integrating New Modules

Future integrations such as Obsidian, Home Assistant, APIs, Internet, local tools, commands, vector stores, and RAG should connect through explicit providers, services, or skill boundaries.

Do not place integration logic directly in pipeline stages.

## Architectural Decisions

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
