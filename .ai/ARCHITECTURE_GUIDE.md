# Architecture Guide

`ARCHITECTURE_GUIDE.md` is the practical companion to `ARCHITECTURE.md`.

Use `ARCHITECTURE.md` for the system overview. Use this guide when deciding where code belongs.

## Dependency Rules

## Allowed Direction

```text
interfaces -> core/bootstrap -> application -> services -> domain
                                     infrastructure -> domain
```

Infrastructure may depend on Domain because it implements Domain contracts.

Application may depend on Services and Domain abstractions.

Domain must remain independent.

## Forbidden Direction

Avoid these dependencies:

```text
domain -> infrastructure
application -> infrastructure concrete classes
services -> interfaces
infrastructure -> interfaces
```

## Layer Guide

## Domain

Use Domain for:

- contracts;
- domain models;
- abstractions that infrastructure must implement.

Correct:

```text
domain/memory.py defines MemoryProvider.
```

Incorrect:

```text
domain imports JsonMemoryProvider.
```

## Application

Use Application for:

- receiving Requests;
- coordinating services;
- returning Responses.

Correct:

```text
Application receives MemoryService.
```

Incorrect:

```text
Application opens data/memory.json directly.
```

## Services

Use Services for:

- application-facing operations;
- wrapping providers behind simple methods;
- keeping use case code clear.

Correct:

```text
MemoryService talks to MemoryProvider.
```

Incorrect:

```text
ConsoleInterface calls MemoryService directly.
```

## Infrastructure

Use Infrastructure for:

- JSON persistence;
- future SQLite adapters;
- future Obsidian adapters;
- external system details.

Correct:

```text
JsonMemoryProvider implements MemoryProvider.
```

Incorrect:

```text
Application imports JsonMemoryProvider.
```

## Core

Use Core for:

- Bootstrap;
- Settings;
- Registry;
- shared Request and Response models.
- Intelligence Pipeline execution and stage orchestration.

Keep package-level exports small to avoid import cycles.

## Interfaces

Use Interfaces for:

- console output;
- future CLI input;
- future API or UI boundaries.

Interfaces should not contain persistence or business rules.

## Practical Checklist

Before adding code, ask:

- Is this a contract or model? Put it in `domain`.
- Is this orchestration? Put it in `application`.
- Is this a service boundary? Put it in `services`.
- Is this concrete persistence or external detail? Put it in `infrastructure`.
- Is this startup wiring? Put it in `core`.
- Is this pre-LLM reasoning? Put it in `core/pipeline`.
- Is this input or output? Put it in `interfaces`.

## Intelligence Pipeline Rule

The Intelligence Pipeline answers "how to think".

Skills answer "how to execute".

LLMs answer "how to write".

Do not put concrete skill execution, external API calls, or provider-specific logic directly inside pipeline stages.

## Import Cycle Rule

If adding a package-level export creates an import cycle, prefer explicit module imports.

Example:

```python
from nyx_local.core.bootstrap import Bootstrap
```

instead of forcing `Bootstrap` through `nyx_local.core`.
