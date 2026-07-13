# Testing

This document describes the current testing baseline.

For coding standards, read `CODE_STYLE.md`.

## Tooling

Nyx Local uses `pytest` for tests.

Static checks:

```powershell
ruff check .
mypy src scripts main.py
```

## Current Coverage Focus

- Request and Response models.
- Application handling.
- Console response rendering.
- Bootstrap initialization and shutdown.
- Registry behavior.
- Settings defaults.
- MemoryService and JsonMemoryProvider.
- Persistent memory between provider instances.
- IntelligencePipeline execution.
- Pipeline stage behavior.
- Gateway Settings and protocol serialization.
- Skill registration, validation, and structured execution errors.
- WebSocket connection, handshake, announcement, heartbeat, reconnect, command dispatch, and shutdown.
- Real Nyx OS Node-to-Python integration for Tool Calling success and structured skill failure.
- PR preparation script command generation.

## Test Guidelines

- Add focused tests for new behavior.
- Use temporary paths for filesystem tests.
- Keep tests tied to Sprint acceptance criteria.
- Avoid broad scaffolding for placeholder-only structure.

## Rule

Testing strategy evolves with future Sprints. Do not add test infrastructure beyond the approved scope.
