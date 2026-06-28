# AI Development Rules

This document defines how humans and AI collaborators should work inside Nyx Local.

For code style, read `CODE_STYLE.md`.

For architecture boundaries, read `ARCHITECTURE_GUIDE.md`.

## Source of Truth

- The `.ai` directory is official project documentation.
- Every Sprint starts by reading `.ai`.
- Architecture decisions belong to the Tech Leader.
- If documentation and code conflict, treat documentation as official and report the mismatch.

## Scope Control

- Implement only the Sprint scope.
- Do not add adjacent capabilities without approval.
- Do not alter architecture by initiative.
- Register improvement ideas as suggestions instead of implementing them directly.

## Sprint Completion

Every Sprint must end with:

- impacted `.ai` documents updated;
- `SPRINT_REPORT.md` updated;
- `Capability Added` section included in the Sprint Report;
- relevant checks executed;
- clean package generated;
- branch prepared for review;
- Pull Request opened when requested.

## Git and Pull Request

- Use `scripts/prepare_pr.py` during delivery preparation.
- Do not merge Pull Requests automatically.
- Do not push unless the user has requested or approved it.
- Pull Requests must clearly explain what changed and why.

## Documentation Responsibility

Each document should answer one primary question.

Avoid duplicating guidance. Prefer cross-references between documents.
