# Capability 05 Changelog

## Extensibility Runtime

Added the official Skills Runtime foundation.

## Added

- `SkillDiscovery` for isolated discovery of Skill factories.
- `SkillRegistry` with manifest-aware registrations.
- `SkillResolver` for resolution by Skill id or capability.
- `SkillExecutor` for execution and standardized error conversion.
- `SkillLifecycle` for `on_load`, `execute`, `on_finish`, and `dispose`.
- `SkillContext`, `SkillManifest`, `SkillRequest`, `SkillRegistration`, and expanded `SkillResult`.
- Skill runtime settings prepared for future discovery sources.
- Bootstrap wiring for all runtime components.
- Focused runtime tests.
- Skills architecture and development guide documentation.

## Not Added

- No real integrations.
- No plugin loading.
- No marketplace.
- No hot reload.
- No LLM integration.
- No user-facing Skill behavior.
