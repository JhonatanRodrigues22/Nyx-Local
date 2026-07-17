# Sprint 25 Changelog - Computer Process List

## Capability Added

Nyx Local now announces and executes `computer.process.list`, the first read-only local
computer capability. The skill returns safe process summaries with `pid`, `name`, and
`status` only.

## Summary

Sprint 25 proves that the Sprint 24 gateway and Skill Runtime can expose a real local
operating-system observation capability without adding control actions or changing protocol
`1.0`.

No Nyx OS code was changed. The existing bridge already accepts `computer.*` capabilities.

## Files Created

- `src/nyx_local/domain/processes.py`
- `src/nyx_local/infrastructure/process_provider.py`
- `src/nyx_local/skills/computer_process_list.py`
- `docs/architecture/COMPUTER_PROCESS_LIST.md`

## Files Changed

- `src/nyx_local/core/bootstrap.py`
- `src/nyx_local/domain/__init__.py`
- `src/nyx_local/infrastructure/__init__.py`
- `src/nyx_local/skills/__init__.py`
- `pyproject.toml`
- `requirements.txt`
- `requirements-dev.txt`
- `tests/test_skills.py`
- `tests/test_bootstrap.py`
- `.ai/STACK.md`
- `README.md`
- `docs/architecture/LOCAL_COMMUNICATION_CLIENT.md`

## Security

- The skill is read-only.
- It does not expose `cmdline`, `cwd`, environment variables, executable paths, or process
  arguments.
- It applies a default and maximum result limit of `200`.
- Values above `200` are capped.
- Invalid limits return structured `INVALID_SKILL_INPUT`.
- Inaccessible individual processes are omitted instead of failing the whole list.

## Dependencies

- Runtime: `psutil==6.1.1`
- Development typing: `types-psutil`

## Validation

- `python -m pytest -q`: 63 passed.
- `python -m ruff check src tests scripts`: passed.
- `python -m mypy src\nyx_local --strict`: passed.

## Git/PR Status

Sprint 25 is implemented on branch `feat/sprint-25-process-list-capability`.
Pull Request: to be opened for human review.

## Manual Integration Expected

1. Run Nyx OS with the Local Gateway enabled.
2. Run Nyx Local with `nyx-local-gateway`.
3. Open `/dev` in Nyx OS.
4. Confirm `local.echo` and `computer.process.list` are visible.
5. Execute `computer.process.list` through the remote Tool Calling path.

## Out of Scope

- Process control.
- Application opening.
- Shell or PowerShell execution.
- Command-line exposure.
- Dedicated Cockpit or Dev Dashboard process UI.
