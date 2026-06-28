# Workflow

This document defines the official Sprint workflow.

For Sprint structure, read `SPRINT_BLUEPRINT.md`.

For delivery review, read `REVIEW_CHECKLIST.md`.

## Mandatory Sprint Flow

Every Sprint must follow this flow:

1. Read the entire `.ai` directory.
2. Read the Sprint prompt.
3. Validate documentation and code consistency.
4. Implement only the approved scope.
5. Update impacted documentation.
6. Update `SPRINT_REPORT.md`.
7. Run relevant checks.
8. Generate a clean package.
9. Prepare the Git/Pull Request flow.
10. Deliver for Tech Leader review.

## Sprint Report Rule

Every Sprint Report must include:

```markdown
## Capability Added
```

This section must describe the new capability gained by Nyx Local during that Sprint.

For documentation-only Meta Sprints, describe the new project or collaboration capability.

## Documentation Rule

After each Sprint, review `.ai` and update only documents that actually changed.

Avoid duplicating content between documents. Prefer cross-references.

## Git and Pull Request Rule

Every Sprint must be reviewed by the Tech Leader before merge.

Use `scripts/prepare_pr.py` to prepare Sprint branches, run tests, generate the clean package, inspect changed files, and receive commit and Pull Request guidance.

Do not merge Pull Requests automatically.

Push and PR actions require explicit user request or approval.
