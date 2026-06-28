# Architecture Guide

Nyx Local uses a layered architecture designed for low coupling and future extension.

## Layers

### Domain

Defines contracts, models, and core concepts.

Allowed dependencies:

- Python standard library.
- Other domain modules when necessary.

Forbidden dependencies:

- `infrastructure`
- concrete providers
- UI or console code
- framework-specific code

### Application

Coordinates use cases and application flow.

Allowed dependencies:

- `domain`
- `services`
- `core` request and response primitives when appropriate

Forbidden dependencies:

- concrete infrastructure implementations such as JSON, SQLite, Obsidian, APIs, or vector stores

### Services

Encapsulates application-facing service boundaries.

Allowed dependencies:

- `domain` contracts
- abstractions injected by Bootstrap

Forbidden dependencies:

- UI rendering
- direct user interaction

### Core

Owns bootstrap, settings, registry, and shared primitives.

Allowed dependencies:

- components required for application wiring

Rule:

Keep package-level exports light to avoid import cycles.

### Infrastructure

Implements contracts defined by `domain`.

Allowed dependencies:

- `domain` contracts and models
- Python standard library

Rule:

Infrastructure may know implementation details. Other layers should not depend on those details.

### Interfaces

Handles input and output boundaries such as console rendering.

Allowed dependencies:

- response models
- application entry points

Forbidden dependencies:

- business rules
- persistence details

## Dependency Direction

Preferred direction:

```text
interfaces -> core/bootstrap -> application -> services -> domain
                                     infrastructure -> domain
```

Domain never knows infrastructure.

Application never depends on concrete providers.

Infrastructure implements contracts defined by Domain.

## Decoupling Principles

- Depend on abstractions when crossing boundaries.
- Register concrete implementations during bootstrap.
- Keep persistence details inside infrastructure.
- Keep rendering details inside interfaces.
- Add abstractions only when they protect a real boundary.
