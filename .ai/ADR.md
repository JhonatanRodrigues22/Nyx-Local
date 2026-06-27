# Architecture Decision Records

## ADR-0001: Initial Python `src/` Layout

Status: Accepted

Decision: The project uses a `src/` layout for production code.

Reason: This keeps production imports separated from repository tooling and prepares the project for packaging.

## ADR-0002: Unified Request and Response Models

Status: Accepted

Decision: Nyx Local uses `Request` and `Response` dataclasses as the shared models for internal application flow.

Reason: A single request and response shape gives future features one stable path through the application without introducing AI, memory, providers, integrations, or business logic in Sprint 02.

## ADR-0003: Sprint Git/Pull Request Preparation Flow

Status: Accepted

Decision: Sprint branches must be prepared through `scripts/prepare_pr.py`, and pushes must wait for Tech Leader review and explicit JJ confirmation.

Reason: The project needs a safe, repeatable review flow that helps prepare branches, tests, packaging, commit guidance, and Pull Request instructions without performing automatic push.

## ADR-0004: Request and Application Naming Refinement

Status: Accepted

Decision: `Request.text` was renamed to `Request.message`, and `Application.process()` was renamed to `Application.handle()`.

Reason: These names better represent conversation-oriented input and application request handling.
