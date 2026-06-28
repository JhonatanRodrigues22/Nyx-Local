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
- PR preparation script command generation.

## Test Guidelines

- Add focused tests for new behavior.
- Use temporary paths for filesystem tests.
- Keep tests tied to Sprint acceptance criteria.
- Avoid broad scaffolding for placeholder-only structure.

## Rule

Testing strategy evolves with future Sprints. Do not add test infrastructure beyond the approved scope.
