# Code Style

## General

- Prefer clear, boring Python.
- Keep modules small and responsibilities focused.
- Use dataclasses for simple data models.
- Use ABCs for stable contracts between layers.
- Avoid overengineering.

## Naming

- Use names that describe the role in the architecture.
- Use `handle()` for application request handling.
- Use `Service` for application service boundaries.
- Use `Provider` for concrete or abstract capability providers.

## File Organization

- Put contracts and domain models in `domain`.
- Put orchestration in `application`.
- Put concrete adapters in `infrastructure`.
- Put bootstrap and shared primitives in `core`.
- Put human or machine interaction boundaries in `interfaces`.
- Put service boundaries in `services`.

## SOLID Guidance

- Single responsibility matters more than clever reuse.
- Prefer dependency injection through constructors or Bootstrap.
- Avoid hidden global state.
- Avoid singletons unless a future Sprint explicitly approves one.

## Documentation

- Document public architectural decisions in `.ai`.
- Keep comments rare and useful.
- Update only documents affected by the Sprint.

## Tests

- Add focused tests for new behavior.
- Test persistence and boundaries when they are part of the Sprint.
- Avoid large test suites for placeholder-only structure.
- Use temporary paths for filesystem tests.
