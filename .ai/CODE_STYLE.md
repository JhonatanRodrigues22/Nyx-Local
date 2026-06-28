# Code Style

`CODE_STYLE.md` is the single official code style reference for Nyx Local.

`CODING_STYLE.md` is retained only as a legacy pointer.

## General Principles

- Prefer clear, simple Python.
- Keep modules focused on one responsibility.
- Avoid overengineering.
- Add abstractions only when they protect a real boundary.
- Keep implementation aligned with `.ai/ARCHITECTURE_GUIDE.md`.

## Naming

- Use `Request` and `Response` for application flow models.
- Use `handle()` for application request handling.
- Use `Service` for application service boundaries.
- Use `Provider` for capability providers.
- Use concrete names for infrastructure implementations, such as `JsonMemoryProvider`.

## File Organization

- `domain`: contracts and domain models.
- `application`: orchestration and request handling.
- `services`: application-facing service boundaries.
- `core`: bootstrap, settings, registry, shared primitives.
- `infrastructure`: concrete adapters.
- `interfaces`: input and output boundaries.
- `tests`: focused automated tests.

## Dataclasses and ABCs

Use dataclasses for plain data models.

Use ABCs when a layer needs to depend on a stable contract instead of a concrete implementation.

## Dependency Injection

Prefer constructor injection or Bootstrap wiring.

Avoid hidden global state.

Avoid singletons unless a future Sprint explicitly approves one.

## Comments and Documentation

- Use comments only when they clarify non-obvious code.
- Record architectural decisions in `ADR.md`.
- Update only documentation affected by the Sprint.
- Keep Sprint documentation consistent with `SPRINT_BLUEPRINT.md`.

## Tests

- Add tests for new behavior.
- Use temporary directories for filesystem persistence tests.
- Keep tests focused on acceptance criteria.
- Do not add broad test scaffolding for placeholder-only structure.

## Formatting and Tools

Use the project configuration in `pyproject.toml`.

Expected local checks:

```powershell
pytest
ruff check .
mypy src scripts main.py
```
