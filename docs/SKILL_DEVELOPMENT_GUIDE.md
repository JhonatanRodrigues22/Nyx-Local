# Skill Development Guide

## Purpose

This guide describes how future Skills should be created for Nyx Local.

No real integration is implemented by this guide. It defines the conventions
future integration Sprints must follow.

## Recommended Structure

Future Skills should keep implementation isolated from the application core.

Recommended shape:

```text
skills/
  example_skill/
    __init__.py
    skill.py
    tests/
```

The first runtime version does not dynamically import this folder yet.

## Contract

Every Skill must extend `Skill`.

```python
from nyx_local.core.skills.interfaces import Skill
from nyx_local.core.skills.models import SkillContext, SkillResult


class ExampleSkill(Skill):
    id = "example"
    name = "Example"
    version = "1.0.0"
    description = "Example Skill."
    capabilities = ["example.read"]
    api_version = "1"

    def execute(
        self,
        context: SkillContext,
        payload: dict[str, object] | None = None,
    ) -> SkillResult:
        return SkillResult(success=True, messages=["Executed."])
```

## Metadata

Each Skill should declare:

- `id`: stable machine-readable identifier;
- `name`: human-readable name;
- `version`: Skill version;
- `description`: short purpose;
- `author`: optional owner;
- `entrypoint`: optional import path for future loaders;
- `permissions`: future permission requirements;
- `capabilities`: actions or domains the Skill supports;
- `api_version`: runtime contract version;
- `enabled`: whether the Skill can be executed.

## Dependency Injection

Skills must receive dependencies through `SkillContext`.

Correct:

```python
memory = context.memory
settings = context.configuration
```

Incorrect:

```python
memory = MemoryService(...)
settings = Settings()
```

Bootstrap and the runtime are responsible for dependency wiring.

## Lifecycle

Skills may override lifecycle hooks when needed:

- `on_load(context)`;
- `execute(context, payload)`;
- `on_finish(context, result)`;
- `dispose(context)`.

Most Skills should only need `execute()` at first.

## Results

All Skills must return `SkillResult`.

Use:

- `messages` for human-readable execution notes;
- `data` for structured output;
- `artifacts` for future files, references, or generated objects;
- `metadata` for diagnostics;
- `errors` for standardized failure details.

## Tests

Skill tests should be isolated.

Use:

- fake contexts;
- explicit payloads;
- temporary paths for filesystem behavior;
- no real external services unless the Sprint explicitly approves them.

## Versioning

Increment Skill `version` when the Skill behavior changes.

Change `api_version` only when the runtime contract changes.

## Future Publication

Future publication may use plugin packages, entry points, marketplace metadata,
or local folders.

Those mechanisms must extend Discovery and Registry without changing Skill
business code.
