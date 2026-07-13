# Sprint Report — Sprint 24 Local Communication Client

## Capability Added

Nyx Local can now operate as a resident local executor for Nyx OS through protocol version `1.0`, announce `local.echo`, receive correlated Tool Calling commands, return structured results, maintain heartbeat, reconnect safely, and shut down cleanly.

## Summary

This Sprint implemented the Python client compatible with the Nyx OS PR #30 local gateway. It added the minimum Skill Runtime required for one technical echo capability and kept the Intelligence Pipeline functionally frozen.

Nyx OS remains the brain and Tool Calling owner. Nyx Local remains the executor.

No operating-system automation, LLM integration, shared memory, shell execution, or cockpit surface was added.

## Files Created

- `src/nyx_local/domain/skills.py`
- `src/nyx_local/domain/gateway.py`
- `src/nyx_local/services/skill_service.py`
- `src/nyx_local/services/gateway_service.py`
- `src/nyx_local/infrastructure/websocket_gateway.py`
- `src/nyx_local/skills/__init__.py`
- `src/nyx_local/skills/local_echo.py`
- `src/nyx_local/gateway_main.py`
- `tests/test_skills.py`
- `tests/test_gateway_settings.py`
- `tests/test_gateway_protocol.py`
- `tests/test_gateway_service.py`
- `tests/test_websocket_gateway.py`
- `tests/integration/nyx_os_gateway.integration.ts`
- `scripts/integration_gateway_client.py`
- `scripts/verify_nyx_os_integration.py`
- `docs/architecture/LOCAL_COMMUNICATION_CLIENT.md`

## Files Changed

- `src/nyx_local/core/settings.py`
- `src/nyx_local/core/bootstrap.py`
- package exports in `domain`, `services`, `infrastructure`, and `core`
- `pyproject.toml`
- `requirements.txt`
- `README.md`
- impacted `.ai` documentation
- `tests/test_bootstrap.py`

## Architecture

- Domain defines skill models, protocol envelopes, connection state, and the transport abstraction.
- Infrastructure implements JSON-over-WebSocket through `websockets`.
- `SkillService` protects the transport from concrete skill exceptions.
- `GatewayService` owns handshake, announcement, heartbeat, command dispatch, reconnect, and shutdown.
- Bootstrap owns all concrete wiring.
- A dedicated SkillRegistry stores executable skills without replacing the existing component Registry.
- The synchronous application entrypoint remains unchanged; `nyx-local-gateway` is separate and asynchronous.

## Security

- `NYX_LOCAL_GATEWAY_TOKEN` is mandatory for resident mode and has no default.
- Tokens are excluded from dataclass representations and logs.
- Gateway URLs are restricted to loopback WebSocket hosts.
- Capability IDs are restricted to `local.*` or `computer.*`.
- Inputs and results are not logged.
- Non-retryable authentication or protocol errors stop reconnect attempts.

## Tests Run

- Existing baseline before new tests: 19 passed.
- Full test suite: 53 passed.
- `ruff check src tests scripts`: passed.
- `mypy src scripts main.py`: passed in strict mode.
- Real Nyx OS Node-to-Python integration: passed.

The real integration started the Nyx OS PR #30 server, launched this Python client, completed handshake and announcement, registered `local.echo`, executed a success through the Nyx OS Tool Calling Engine, then validated a structured Python skill failure with full correlation and protocol-safe error details before disconnecting and cleaning up.

## Packaging Status

`scripts/package_project.py` completed successfully and generated `dist/nyx_local_project.zip`. The archive excludes `.venv`, Git metadata, caches, logs, build directories, and nested archives.

## Git/PR Status

Repository history is preserved from `main`. Sprint 24 is published on branch `codex/sprint-24-local-communication-client` in Draft PR [#8](https://github.com/JhonatanRodrigues22/Nyx-Local/pull/8); merge remains a human decision.

## Sprint 25 Suggestions

- Define per-skill execution timeout and cooperative cancellation semantics before adding operating-system automation.
- Evaluate isolated/concurrent execution for long-running skills so future executors cannot delay heartbeat processing.

These suggestions are intentionally not implemented in Sprint 24.

## Limitations

- Only the technical `local.echo` skill exists.
- No operating-system automation exists.
- Skill execution has no internal timeout or cancellation yet.
- The registry is in memory and discovery is explicit through Bootstrap.
- Transport is local WebSocket without TLS.
- The Intelligence Pipeline is not integrated with gateway commands.
