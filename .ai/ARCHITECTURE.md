# Architecture

## Current Structure

The project uses a Python `src/` layout.

## Packages

- `core`: Future shared foundation primitives.
- `domain`: Future domain concepts and rules.
- `application`: Future use cases and orchestration.
- `infrastructure`: Future external adapters and implementation details.
- `interfaces`: Future input and output boundaries.

## Sprint 02 Internal Flow

The first internal flow is:

1. User
2. Application
3. Core
4. Response
5. Interface

The current implementation establishes:

- `Request`: Unified request model in `core`.
- `Response`: Unified response model in `core`.
- `Application`: Initial application orchestrator.
- `App`: Application bootstrap and execution entry point.

## Sprint 02.5 Refinements

- `Request.message` is the official user input field.
- `Application.handle()` is the official application handler method.
- `ConsoleInterface` is the console output boundary for rendering responses.

## Sprint 03 Application Infrastructure

The application initialization flow is:

1. `main`
2. `Bootstrap`
3. `App`
4. `Application`
5. `ConsoleInterface`

The current implementation establishes:

- `Bootstrap`: Initializes settings, registry, application, console interface, and app.
- `Settings`: Dataclass for current and future application configuration.
- `Registry`: Simple component registry for bootstrap wiring.
- `services`: Reserved package for future application services.

## Sprint 04 Memory Foundation

The first persistent memory flow is:

1. CLI
2. `Application`
3. `MemoryService`
4. `MemoryProvider`
5. `JsonMemoryProvider`
6. `data/memory.json`

The current implementation establishes:

- `MemoryProvider`: Domain interface for memory operations.
- `MemoryEntry`: Domain model for stored memory values.
- `JsonMemoryProvider`: Infrastructure provider backed by JSON.
- `MemoryService`: Service boundary used by application code.
- `Settings.memory`: Configuration for memory provider and path.

`Application` may depend on `MemoryService`, but it must not depend on `JsonMemoryProvider` or JSON persistence details.

## Rule

Architecture must not be changed without approval from the Tech Leader.
