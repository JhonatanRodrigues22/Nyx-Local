# Architecture

`ARCHITECTURE.md` is the high-level architectural overview of Nyx Local.

For practical dependency rules and examples, read `ARCHITECTURE_GUIDE.md`.

## Philosophy

Nyx Local is designed as a local-first, layered Python application. Each layer has a clear responsibility and communicates through explicit boundaries.

The architecture favors:

- low coupling;
- simple dependency direction;
- replaceable infrastructure;
- small capabilities delivered through Sprints;
- documentation as part of the system architecture.

## System Overview

```text
User / CLI
    |
Interfaces
    |
Core / Bootstrap
    |
Application
    |
Services
    |
Domain contracts and models
    |
Infrastructure implementations
```

## Runtime Flow

The current application startup flow is:

```text
main -> Bootstrap -> App -> Application -> ConsoleInterface
```

Bootstrap owns concrete wiring:

- creates `Settings`;
- creates `Registry`;
- creates services and concrete providers;
- creates `Application`;
- creates `ConsoleInterface`;
- creates `App`;
- registers components.

The resident local communication flow is separate from request handling:

```text
Nyx OS -> WebSocketGateway -> GatewayService -> SkillService -> SkillRegistry -> local.echo
```

Nyx OS is the brain and Tool Calling owner. Nyx Local is the executor. The gateway does not call the Intelligence Pipeline.

## Memory Flow

The current memory flow is:

```text
Application -> MemoryService -> MemoryProvider -> JsonMemoryProvider -> data/memory.json
```

Application may use `MemoryService`, but it must not know JSON persistence details.

## Intelligence Flow

The current Intelligence Pipeline flow is:

```text
Input -> Normalizer -> Intent Detection -> Context Builder -> Memory Retrieval
      -> Project Retrieval -> Reasoning Planner -> Prompt Composer
      -> Future LLM -> Response Validator
```

The Pipeline prepares reasoning before any future LLM call.

Responsibility split:

- Pipeline thinks.
- LLM writes.
- Skills execute.

Detailed documentation lives in `docs/architecture/INTELLIGENCE_ARCHITECTURE.md`.

## Layer Responsibilities

- `interfaces`: input and output boundaries.
- `core`: bootstrap, settings, registry, request and response primitives.
- `application`: application orchestration.
- `services`: service boundaries used by application code.
- `domain`: contracts, models, and domain concepts.
- `infrastructure`: concrete adapters that implement domain contracts.

## Principles

- Domain never depends on Infrastructure.
- Application does not depend on concrete providers.
- Infrastructure implements contracts defined by Domain.
- Bootstrap wires concrete implementations.
- Interfaces render or receive data but do not own business rules.
- New capabilities should extend the system without forcing unrelated layers to change.

## Current Capabilities

- Structured project foundation.
- Request and Response models.
- Application handler flow.
- Console rendering boundary.
- Bootstrap and component Registry.
- Settings dataclass.
- JSON-backed persistent memory foundation.
- Intelligence Pipeline foundation.
- Nyx OS WebSocket gateway client.
- Minimal Skill Runtime with `local.echo`.
- AI collaboration documentation.
