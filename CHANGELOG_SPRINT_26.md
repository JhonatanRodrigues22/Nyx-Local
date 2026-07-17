# Sprint 26 Changelog - Application Open

## Capability Added

Nyx Local now announces and executes `computer.application.open`, the first local capability
that performs an action on the computer.

## Summary

The skill opens applications from a hardcoded symbolic allowlist. It never accepts executable
paths, arbitrary commands, shell flags, working directories, or free arguments from input.

No Nyx OS code was changed. The existing Sprint 24 bridge accepts `computer.*` capabilities
and exposes them through Tool Calling.

## Allowlist

- `vscode`
- `file-explorer`
- `notepad`

## Files Created

- `src/nyx_local/domain/applications.py`
- `src/nyx_local/infrastructure/application_provider.py`
- `src/nyx_local/skills/computer_application_open.py`
- `docs/architecture/COMPUTER_APPLICATION_OPEN.md`

## Files Changed

- `src/nyx_local/core/bootstrap.py`
- `src/nyx_local/domain/__init__.py`
- `src/nyx_local/infrastructure/__init__.py`
- `src/nyx_local/skills/__init__.py`
- `tests/test_skills.py`
- `tests/test_bootstrap.py`
- `README.md`
- `docs/architecture/LOCAL_COMMUNICATION_CLIENT.md`

## Security

- Hardcoded allowlist only.
- No executable paths from input.
- No arbitrary shell commands.
- No free arguments.
- Unknown apps return `APP_NOT_ALLOWED`.
- Provider failures return `APP_OPEN_FAILED`.
- Responses do not expose real commands, paths, shell output, or stack traces.

## Validation

- `python -m pytest -q`: 78 passed.
- `python -m ruff check src tests scripts`: passed.
- `python -m mypy src\nyx_local --strict`: passed.

## Git/PR Status

Sprint 26 is implemented on branch `feat/sprint-26-application-open-capability`.
Pull Request: to be opened for human review.
