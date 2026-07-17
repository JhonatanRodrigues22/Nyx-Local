# Computer Application Open Capability

## Purpose

`computer.application.open` is the first Nyx Local capability that performs an action on the
computer. It opens a known application from a hardcoded symbolic allowlist.

The skill does not execute arbitrary commands. It does not accept paths. It does not accept
arguments.

## Security Model

Every local capability is announced to Nyx OS and can become callable by the AI through Tool
Calling. For that reason, accepting a user-provided executable path, shell command, or free
argument would create an avoidable prompt-injection risk.

Sprint 26 uses the safer design:

```text
hardcoded allowlist + symbolic name + no free arguments
```

Adding a new application requires a code change and human PR review.

## Allowlist

The allowlist is defined in `src/nyx_local/domain/applications.py`.

| Symbolic name | Real command |
| --- | --- |
| `vscode` | `code` |
| `file-explorer` | `explorer.exe` |
| `notepad` | `notepad.exe` |

The real command is never returned in skill output.

## Input Contract

```json
{
  "app": "notepad"
}
```

Rules:

- `app` is required.
- `app` must be a non-empty string.
- `app` must match the allowlist exactly.
- Fields such as `path`, `command`, `args`, `arguments`, `cwd`, and `shell` have no
  execution effect.

## Output Contract

Success:

```json
{
  "app": "notepad",
  "opened": true
}
```

Skill-level failure codes:

- `INVALID_SKILL_INPUT`
- `APP_NOT_ALLOWED`
- `APP_OPEN_FAILED`

At the gateway protocol boundary, local skill failures are wrapped as `REMOTE_COMMAND_FAILED`
with the original skill code preserved in safe details as `internalCode`.

The skill never returns:

- real command
- executable path
- command arguments
- shell output
- stack trace
- sensitive system details

## Implementation

`ComputerApplicationOpenSkill` validates input and resolves the symbolic name from the
allowlist. `SubprocessApplicationProvider` opens the approved command with:

```text
shell=False
stdin/stdout/stderr=DEVNULL
close_fds=True
```

The provider receives only an `ApplicationOpenSpec`; it never receives raw input fields from
the request.

## Out of Scope

- Opening URLs.
- Passing files, folders, or arguments.
- Running shell, PowerShell, scripts, or terminal commands.
- Killing or closing applications.
- Dynamic runtime allowlists.
- Cockpit confirmation UI.
- Dedicated app-opening UI.

## Validation

Required checks:

```powershell
pytest
ruff check src tests scripts
mypy src\nyx_local --strict
```

Manual integration:

1. Start Nyx OS with the Local Gateway enabled.
2. Start Nyx Local with `nyx-local-gateway`.
3. Confirm `/api/dev/snapshot` shows `computer.application.open`.
4. Execute `computer.application.open` with an allowed app.
5. Execute it with an unknown app and confirm structured `APP_NOT_ALLOWED`.
