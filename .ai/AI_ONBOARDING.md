# AI Onboarding

This is the entry point for any AI or human collaborator joining Nyx Local.

## Project Vision

Nyx Local is a local-first Python application prepared for modular growth. The project evolves through small Sprints that add clear capabilities while preserving a clean layered architecture.

## Current Goal

Build a stable local application foundation before adding advanced capabilities. Features must be introduced only when a Sprint explicitly authorizes them.

## Architecture Summary

Nyx Local uses a layered `src/` layout:

- `domain`: Contracts, models, and business concepts. It must not depend on infrastructure.
- `application`: Use case orchestration. It depends on abstractions and services, not concrete infrastructure.
- `services`: Application service boundaries.
- `core`: Bootstrap, settings, registry, request and response primitives.
- `infrastructure`: Concrete adapters that implement contracts.
- `interfaces`: Input and output boundaries.

## Development Flow

Before any implementation:

1. Read the entire `.ai` directory.
2. Read the Sprint prompt.
3. Check for conflicts between documentation and code.
4. Follow the documented architecture.

After implementation:

1. Update only the documentation that actually changed.
2. Run the relevant checks.
3. Generate the clean package.
4. Prepare the Git/Pull Request flow.
5. Deliver for Tech Leader review.

## Important Documents

- `00_INDEX.md`: Map of institutional knowledge.
- `PROJECT.md`: Project identity and current phase.
- `ARCHITECTURE.md`: Official architecture history.
- `ARCHITECTURE_GUIDE.md`: Layer rules and dependency guidance.
- `WORKFLOW.md`: Mandatory Sprint workflow.
- `SPRINT_BLUEPRINT.md`: Template for future Sprints.
- `CODE_STYLE.md`: Coding and testing standards.
- `REVIEW_CHECKLIST.md`: Pull Request review checklist.
- `DO_NOT.md`: Explicit restrictions.

## Collaboration Rule

Documentation is the source of truth. If code and `.ai` documentation conflict, follow `.ai` and register the inconsistency for Tech Leader review.
