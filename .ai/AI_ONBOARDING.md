# AI Onboarding

This is the entry point for any AI or human collaborator joining Nyx Local.

## What Nyx Local Is

Nyx Local is a local-first Python application designed to grow through small, explicit Sprints.

The project values:

- clarity;
- low coupling;
- documentation as source of truth;
- conservative architecture changes;
- collaboration between humans and AI contributors.

## What Exists Today

Nyx Local currently includes:

- a layered Python structure;
- Bootstrap, Settings, Registry, App, Application, and ConsoleInterface;
- Request and Response models;
- a JSON-backed persistent memory foundation;
- a stage-based Intelligence Pipeline for pre-LLM reasoning;
- a Skills Runtime foundation for future extensibility;
- Git/Pull Request workflow support;
- an `.ai` knowledge base for onboarding and governance.

## First Reading Path

Read these documents in order:

1. `00_INDEX.md`
2. `PROJECT.md`
3. `STACK.md`
4. `ARCHITECTURE.md`
5. `WORKFLOW.md`
6. `SPRINT_BLUEPRINT.md`
7. `DEVELOPMENT_RULES.md`
8. `CODE_STYLE.md`
9. `REVIEW_CHECKLIST.md`

## How to Start a Sprint

1. Read the full `.ai` directory.
2. Read the Sprint prompt.
3. Check whether documentation and code agree.
4. Implement only the approved scope.
5. Update impacted documentation.
6. Run checks and generate the package.
7. Prepare a branch and Pull Request for review.

## Source of Truth

If code and `.ai` documentation conflict, follow `.ai` and record the inconsistency for Tech Leader review.

## Important Boundaries

- Domain must not depend on Infrastructure.
- Application must not depend on concrete providers.
- Bootstrap owns concrete wiring.
- Infrastructure implements Domain contracts.
- Interfaces handle input/output only.
