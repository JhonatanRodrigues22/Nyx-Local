# Skills Architecture

## Overview

The Skills Runtime is the official extensibility boundary of Nyx Local.

It prepares the project so future capabilities such as Obsidian, Gmail, Calendar,
local tools, browser automation, and workflow automation can be added as
independent Skills without changing the application core.

This architecture does not implement real integrations. It only defines the
runtime needed to discover, register, resolve, execute, and manage Skill
lifecycle behavior.

## Responsibility Flow

```text
Discovery
  |
Registry
  |
Resolver
  |
Executor
  |
Lifecycle
  |
SkillResult
```

## Discovery

`SkillDiscovery` is responsible only for finding Skill factories.

The current implementation supports explicit candidate factories and keeps
`search_paths` as configuration for future discovery sources.

Future sources may include:

- local `skills/` folders;
- plugin folders;
- Python packages;
- entry points;
- marketplace metadata.

Discovery must not register, resolve, or execute Skills.

## Registry

`SkillRegistry` stores Skill metadata and factories.

It owns:

- Skill ids;
- manifests;
- factory references;
- available Skill listings.

It must not execute Skills or load external dependencies.

## Resolver

`SkillResolver` receives a `SkillRequest` and returns a `SkillRegistration`.

It can resolve by:

- explicit `skill_id`;
- declared capability.

Resolution failures use standardized runtime errors and can be converted into
`SkillResult` failures by `SkillManager`.

## Executor

`SkillExecutor` is responsible for execution only.

Execution flow:

```text
validate manifest
  |
instantiate Skill
  |
on_load()
  |
execute()
  |
on_finish()
  |
dispose()
  |
SkillResult
```

The executor captures runtime exceptions and converts them into failed
`SkillResult` objects.

## Lifecycle

`SkillLifecycle` coordinates lifecycle hooks:

- `on_load(context)`;
- `execute(context, payload)`;
- `on_finish(context, result)`;
- `dispose(context)`.

Hooks are intentionally small and synchronous in the first runtime version.

## Skill Context

`SkillContext` is the dependency injection boundary for Skills.

Skills should not instantiate application services directly. Instead, runtime
wiring must pass dependencies through context fields such as:

- user;
- configuration;
- memory;
- projects;
- services;
- logger;
- metadata;
- cancellation token;
- execution information.

## Skill Result

`SkillResult` is the standard result shape for every Skill.

It contains:

- `success`;
- `data`;
- `messages`;
- `artifacts`;
- `metadata`;
- `execution_time`;
- `errors`.

This keeps Skill outputs predictable for future Application, Pipeline, and UI
coordination.

## Manifest

`SkillManifest` describes each Skill before execution.

It contains:

- `id`;
- `name`;
- `version`;
- `description`;
- `author`;
- `entrypoint`;
- `permissions`;
- `capabilities`;
- `api_version`;
- `enabled`.

The first implementation uses Python classes instead of JSON manifests. This
keeps the runtime simple while preserving the same metadata contract.

## Versioning

Every Skill declares:

- Skill version through `version`;
- Runtime API version through `api_version`.

Only API version `1` exists today.

## Hot Reload

Hot reload is not implemented.

The architecture allows it later by changing Discovery to watch sources and
refresh Registry entries:

```text
new Skill appears
  |
Discovery detects it
  |
Registry updates metadata
  |
Resolver can select it
  |
Executor can run it
```

## Relationship With Pipeline

The Intelligence Pipeline prepares reasoning.

Skills execute concrete actions.

The Pipeline must not contain integration logic. Future stages may prepare a
Skill request, but execution belongs to the Skills Runtime.

## Testability

The runtime supports isolated tests through:

- fake Skill classes;
- explicit discovery candidates;
- in-memory registry instances;
- fake `SkillContext` objects;
- direct executor tests.
