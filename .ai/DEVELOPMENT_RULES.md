# AI Development Rules

## Source of Truth

- The `.ai` directory is official project documentation.
- Every collaborator must read `.ai` before starting a Sprint.
- Architecture decisions belong to the Tech Leader.
- Implementation must follow approved documentation.

## Scope Control

- Implement only what the Sprint authorizes.
- Do not add adjacent capabilities because they seem useful.
- Do not change architecture without approval.
- If a better architecture is identified, register it as a suggestion.

## Sprint Completion

- Update only impacted `.ai` documents.
- Update `SPRINT_REPORT.md`.
- Run the relevant checks.
- Generate `dist/nyx_local_project.zip`.
- Prepare a branch and Pull Request for review.

## Git and Pull Request

- Use `scripts/prepare_pr.py` to prepare Sprint branches.
- Do not push before the work is ready for review.
- Do not merge Pull Requests automatically.
- Pull Requests must summarize the Sprint clearly.
- Push requires explicit JJ confirmation when not directly requested.
