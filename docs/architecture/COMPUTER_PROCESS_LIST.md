# Computer Process List Capability

## Purpose

`computer.process.list` is the first real local computer capability exposed by Nyx Local.
It is read-only and exists to prove that Nyx OS can observe a small, safe part of the local
environment through the Sprint 24 gateway.

It does not control the computer.

## Capability

ID:

```text
computer.process.list
```

Input:

```json
{
  "limit": 200
}
```

`limit` is optional. The default is `200`, and the maximum is `200`. Values above the
maximum are capped. Non-integer, boolean, zero, or negative values return structured
`INVALID_SKILL_INPUT`.

Output:

```json
{
  "processes": [
    {
      "pid": 1234,
      "name": "Code.exe",
      "status": "running"
    }
  ],
  "count": 1,
  "limit": 200,
  "truncated": false
}
```

`count` is the number of returned processes. `truncated` is `true` when more processes
exist than the applied limit.

## Safety Boundaries

The MVP returns only:

- `pid`
- `name`
- `status`

The skill never returns by default:

- command-line arguments
- current working directory
- environment variables
- executable path
- shell output
- user tokens or flags derived from process arguments

This is intentional because command lines and environment variables often contain secrets.
Any future exposure of those fields needs a separate opt-in design and security review.

## Implementation

`ComputerProcessListSkill` lives in `src/nyx_local/skills/computer_process_list.py`.
It depends on the `ProcessProvider` protocol and is wired in `Bootstrap` with
`PsutilProcessProvider`.

`PsutilProcessProvider` uses `psutil.process_iter(attrs=["pid", "name", "status"])`.
It omits processes that raise `AccessDenied`, `NoSuchProcess`, or `ZombieProcess`.
One inaccessible process cannot fail the entire skill execution.

The process list is sorted by `pid` for stable, predictable output. No CPU-based ordering is
used, because CPU sampling is interval-dependent and unstable across environments.

## Nyx OS Impact

No Nyx OS code change is required for Sprint 25. The Sprint 24 bridge already accepts
`computer.*` capability IDs and registers remote capabilities through the existing Tool
Calling path.

If a future run requires Nyx OS changes for this capability, that is a bridge issue and
should be investigated separately before implementation.

## Validation

Required checks:

```powershell
pytest
ruff check src tests scripts
mypy src\nyx_local --strict
```

Manual integration:

1. Start Nyx OS with `NYX_ENABLE_LOCAL_GATEWAY=true` and the shared token.
2. Start Nyx Local with `nyx-local-gateway`.
3. Open `http://localhost:3000/dev`.
4. Confirm `local.echo` and `computer.process.list` are announced.
5. Execute `computer.process.list` through the remote Tool Calling path and confirm the
   output contract above.
