# Local Communication Client

## Purpose

Nyx Local is the local executor for Nyx OS. Sprint 24 adds a resident WebSocket client that connects to the Nyx OS local gateway and exposes a minimal technical skill, `local.echo`. Sprint 25 keeps protocol `1.0` and adds the first read-only computer observation skill, `computer.process.list`.

Nyx OS remains the brain and owns Tool Calling. Nyx Local owns local execution. The Intelligence Pipeline is not connected to the gateway in this Sprint.

## Runtime Flow

```text
Nyx OS Tool Calling Engine
    -> WebSocket local.command.request
    -> GatewayService
    -> SkillService
    -> SkillRegistry
    -> local.echo / computer.process.list
    -> WebSocket local.command.result
```

`Bootstrap` wires the existing synchronous application and the new resident components. The `nyx-local` entrypoint remains synchronous. The separate `nyx-local-gateway` entrypoint owns the asynchronous resident lifecycle.

## Protocol

- URL: `ws://127.0.0.1:4789` by default.
- Version: `1.0` on every envelope.
- Authentication: `NYX_LOCAL_GATEWAY_TOKEN`, with no default.
- Allowed capability prefixes: `local.` and `computer.`.

The session order is:

1. connect;
2. send `local.handshake`;
3. require `local.handshake.accepted`;
4. send `local.capabilities.announcement`;
5. start one heartbeat task;
6. receive and dispatch command requests;
7. send correlated command results;
8. close and clean up tasks on shutdown.

Authentication and incompatible-protocol errors marked non-retryable stop the resident client. Retryable transport failures reconnect with exponential backoff from 1 second up to the configured maximum. Backoff resets after an accepted handshake.

## Layers

- `domain/skills.py`: Skill contracts, descriptors, structured results, and the dedicated SkillRegistry.
- `domain/gateway.py`: protocol dataclasses and the transport abstraction.
- `services/skill_service.py`: safe skill resolution and execution.
- `services/gateway_service.py`: protocol and connection lifecycle orchestration.
- `infrastructure/websocket_gateway.py`: concrete JSON-over-WebSocket adapter.
- `infrastructure/process_provider.py`: `psutil` adapter that omits inaccessible processes.
- `skills/local_echo.py`: technical echo skill.
- `skills/computer_process_list.py`: read-only process list skill.
- `core/settings.py`: environment-backed gateway configuration.
- `core/bootstrap.py`: concrete dependency wiring.
- `gateway_main.py`: resident entrypoint.

The core `Registry` remains the component container. `SkillRegistry` is narrower and stores only executable skills; it does not replace or duplicate the core registry.

## Settings

Supported environment variables:

- `NYX_LOCAL_GATEWAY_URL`
- `NYX_LOCAL_GATEWAY_TOKEN`
- `NYX_LOCAL_INSTANCE_ID`
- `NYX_LOCAL_HEARTBEAT_INTERVAL_SECONDS`
- `NYX_LOCAL_RECONNECT_MAX_SECONDS`

The URL is restricted to loopback WebSocket hosts. The token is excluded from dataclass representations and logs. If `NYX_LOCAL_INSTANCE_ID` is absent, a deterministic hostname-based ID is used, so restarts do not create a new identity.

## Skill Contract

`local.echo` accepts:

```json
{"message": "hello"}
```

and returns:

```json
{"message": "hello"}
```

Invalid input, unknown skills, and execution exceptions become structured results. Skill exceptions never escape to the gateway lifecycle.

`computer.process.list` accepts optional input:

```json
{"limit": 200}
```

The skill returns only `pid`, `name`, and `status`, plus `count`, `limit`, and `truncated`.
It never returns command lines, current working directories, environment variables, executable
paths, or process arguments. The default and maximum limit is `200`; values above `200` are
capped, and non-integer or non-positive values return structured `INVALID_SKILL_INPUT`.
Individual inaccessible processes are omitted so one denied process cannot fail the whole list.

`SKILL_NOT_FOUND` and `INVALID_SKILL_INPUT` are internal Skill Runtime reasons, not protocol 1.0 error codes. At the network boundary they are mapped to `REMOTE_COMMAND_FAILED`; the original reason is retained in `error.details.internalCode`, together with safe primitive details. Incoming structured errors validate `code`, `message`, `retryable`, and `details` at runtime.

## Validation

The normal checks are:

```powershell
pytest
ruff check src tests scripts
mypy src scripts main.py
python -m nyx_local.main
```

Real Node-to-Python integration against a Nyx OS checkout containing PR #30 is available through:

```powershell
python scripts/verify_nyx_os_integration.py --nyx-os C:\path\to\Nyx-OS
```

The verifier temporarily installs a Jest harness in the Nyx OS checkout, runs real success and structured-failure round-trips, and removes the harness in a `finally` block. The failure path validates `requestId`, `capabilityId`, public error code, retryability, and details across Node and Python.

GitHub Actions runs `pytest`, Ruff, and strict mypy checks for pull requests and pushes to `main`.

## Out of Scope

- Windows or operating-system automation beyond read-only process observation.
- Application, mouse, keyboard, clipboard, screenshot, OCR, shell, or PowerShell execution.
- Process control, process killing, process pausing, or command-line exposure.
- Intelligence Pipeline integration.
- LLM, prompts, or intent handling.
- Shared memory.
- External networking, TLS, GUI, or cockpit surfaces.
