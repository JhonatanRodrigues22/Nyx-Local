# Architecture Decision Records

## ADR-0001: Initial Python `src/` Layout

Status: Accepted

Decision: The project uses a `src/` layout for production code.

Reason: This keeps production imports separated from repository tooling and prepares the project for packaging.

## ADR-0002: Unified Request and Response Models

Status: Accepted

Decision: Nyx Local uses `Request` and `Response` dataclasses as the shared models for internal application flow.

Reason: A single request and response shape gives future features one stable path through the application.

## ADR-0003: Sprint Git/Pull Request Preparation Flow

Status: Accepted

Decision: Sprint branches must be prepared through `scripts/prepare_pr.py`, and pushes must wait for review and explicit approval.

Reason: The project needs a safe, repeatable review flow that helps prepare branches, tests, packaging, commit guidance, and Pull Request instructions without automatic push.

## ADR-0004: Request and Application Naming Refinement

Status: Accepted

Decision: `Request.text` was renamed to `Request.message`, and `Application.process()` was renamed to `Application.handle()`.

Reason: These names better represent conversation-oriented input and application request handling.

## ADR-0005: Bootstrap, Settings, and Registry Foundation

Status: Accepted

Decision: Nyx Local uses a `Bootstrap` class to initialize application components, a `Settings` dataclass for configuration defaults, and a simple `Registry` for component registration and lookup.

Reason: This establishes a clear startup path for future capabilities.

## ADR-0006: Memory Provider Abstraction with JSON Persistence

Status: Accepted

Decision: Nyx Local uses a domain-level `MemoryProvider` abstraction, a `MemoryService` boundary, and an initial `JsonMemoryProvider` infrastructure implementation that persists entries in `data/memory.json`.

Reason: This gives the project persistent memory while keeping the architecture prepared for future providers such as SQLite, Obsidian, or vector storage.

## ADR-0007: AI Development Framework Documentation

Status: Accepted

Decision: Nyx Local maintains dedicated AI development framework documentation inside `.ai`, including onboarding, Sprint blueprint, architecture guide, code style, development rules, and review checklist documents.

Reason: The project needs reusable institutional guidance so human and AI collaborators can contribute consistently without relying on external context.

## ADR-0008: Documentation Responsibility Model

Status: Accepted

Decision: Nyx Local documentation follows a responsibility model: `README.md` introduces the project, `ARCHITECTURE.md` explains the high-level system, `ARCHITECTURE_GUIDE.md` gives practical rules, `CODE_STYLE.md` is the official style reference, and `SPRINT_BLUEPRINT.md` defines future Sprint structure.

Reason: Documentation should behave like architecture: each document should answer a clear question without competing with another document.

## ADR-0009: Stage-Based Intelligence Pipeline

Status: Accepted

Decision: Nyx Local uses a stage-based Intelligence Pipeline in `core/pipeline` to prepare reasoning before any future LLM call.

Reason: The project needs a modular place for normalization, intent detection, context building, retrieval, planning, prompt composition, and response validation without giving the future LLM ownership of application logic.

Consequence: Pipeline stages must remain focused on reasoning preparation. Skills and concrete execution logic must stay outside the Pipeline.

## ADR-0010: Pipeline Builder and Stage Registry

Status: Accepted

Decision: `IntelligencePipeline` no longer creates stages directly. `PipelineBuilder` and `StageRegistry` own stage construction, metadata filtering, and priority ordering.

Reason: Pipeline execution should stay decoupled from stage assembly so future configuration, plugins, debugging, and dynamic loading can evolve without changing pipeline execution.

## ADR-0011: Skills Infrastructure Boundary

Status: Accepted

Decision: Nyx Local has an initial Skills infrastructure with `Skill`, `SkillRegistry`, `SkillManager`, and `SkillResult`, but no user-facing Skill behavior.

Reason: The project needs a clear boundary before future executable integrations are added. Pipeline thinks; Skills execute.

## ADR-0012: Official Skills Runtime

Status: Accepted

Decision: Nyx Local uses `core/skills` as the official extensibility runtime with
separate Discovery, Registry, Resolver, Executor, Lifecycle, Context, Manifest,
Request, Registration, and Result responsibilities.

Reason: Future integrations must be added as independent Skills without changing
the application core or mixing execution logic into the Intelligence Pipeline.

Consequence: Real integrations, plugin loading, marketplace behavior, and hot
reload remain future capabilities. This runtime only establishes the contract and
execution boundary.
