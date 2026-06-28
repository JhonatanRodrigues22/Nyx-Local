# Nyx Local

Nyx Local is a local-first Python application built through small, reviewable Sprints. The project is designed for long-term collaboration between humans and AI contributors, with strong documentation, explicit architecture boundaries, and a conservative development workflow.

## Overview

Nyx Local currently provides the foundation for a modular local application:

- a layered Python package structure;
- a Bootstrap-driven startup flow;
- shared Request and Response models;
- a console output boundary;
- a simple dependency Registry;
- application Settings;
- a JSON-backed persistent memory foundation;
- an official `.ai` knowledge base for future collaborators.

## Goals

- Keep the project local-first and easy to run.
- Preserve clean separation between layers.
- Add capabilities through explicit Sprints.
- Keep application code independent from concrete infrastructure details.
- Make the repository understandable to future human and AI contributors.

## Current Status

The project has completed its foundation phase and now includes first memory support through a JSON provider.

Current implemented capabilities:

- Application bootstrap and shutdown flow.
- Request handling through `Application`.
- Response rendering through `ConsoleInterface`.
- Component registration through `Registry`.
- Application configuration through `Settings`.
- Persistent key-value memory through `MemoryService` and `JsonMemoryProvider`.
- AI collaboration documentation in `.ai`.

Not implemented yet:

- LLM integration.
- SQLite memory.
- Obsidian integration.
- embeddings or vector memory.
- semantic search.
- skills or providers beyond the current JSON memory provider.

## Architecture Summary

Nyx Local follows a layered architecture:

```text
Interfaces
    |
Core / Bootstrap
    |
Application
    |
Services
    |
Domain contracts
    |
Infrastructure implementations
```

Core flow:

```text
main -> Bootstrap -> App -> Application -> ConsoleInterface
```

Memory flow:

```text
Application -> MemoryService -> MemoryProvider -> JsonMemoryProvider -> data/memory.json
```

For the high-level architecture, read `.ai/ARCHITECTURE.md`.

For practical dependency rules and examples, read `.ai/ARCHITECTURE_GUIDE.md`.

## How to Run

Python 3.13 or newer is required.

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt
python main.py
```

## Tests and Checks

```powershell
pytest
ruff check .
mypy src scripts main.py
```

## Packaging

Generate a clean project package:

```powershell
python scripts/package_project.py
```

Output:

```text
dist/nyx_local_project.zip
```

## Project Structure

- `.ai/`: official institutional knowledge for humans and AI collaborators.
- `config/`: future configuration templates.
- `data/`: local runtime data files such as `memory.json`.
- `docs/`: project documentation outside the AI knowledge base.
- `scripts/`: development and delivery helpers.
- `src/nyx_local/application/`: application orchestration.
- `src/nyx_local/core/`: bootstrap, settings, registry, and shared primitives.
- `src/nyx_local/domain/`: contracts and domain models.
- `src/nyx_local/infrastructure/`: concrete adapter implementations.
- `src/nyx_local/interfaces/`: input and output boundaries.
- `src/nyx_local/services/`: application service boundaries.
- `tests/`: automated tests.

## Documentation

Start here:

1. `.ai/00_INDEX.md`
2. `.ai/AI_ONBOARDING.md`
3. `.ai/PROJECT.md`
4. `.ai/STACK.md`
5. `.ai/ARCHITECTURE.md`
6. `.ai/WORKFLOW.md`
7. `.ai/SPRINT_BLUEPRINT.md`
8. `.ai/DEVELOPMENT_RULES.md`

Useful references:

- `.ai/CODE_STYLE.md`
- `.ai/ARCHITECTURE_GUIDE.md`
- `.ai/REVIEW_CHECKLIST.md`
- `.ai/ADR.md`
- `.ai/ROADMAP.md`

## Git / Pull Request Flow

Prepare a Sprint branch for review:

```powershell
python scripts/prepare_pr.py branch-name
```

The script verifies Git, creates or switches branch, runs tests, generates the clean package, shows changed files, and prints commit and Pull Request guidance.

No automatic push or Pull Request merge should happen without explicit approval.

## Roadmap

Completed:

- project structure;
- operational workflow;
- core request/response flow;
- Git/Pull Request preparation;
- Bootstrap and application infrastructure;
- JSON-backed memory foundation;
- AI development documentation.

Future work may include richer local memory providers, user-facing interfaces, skills, providers, and AI integration, only when approved by future Sprints.

## Contributing

Before contributing:

1. Read the `.ai` directory.
2. Follow `.ai/SPRINT_BLUEPRINT.md`.
3. Respect `.ai/ARCHITECTURE_GUIDE.md`.
4. Use `.ai/CODE_STYLE.md`.
5. Check `.ai/REVIEW_CHECKLIST.md` before opening a Pull Request.
