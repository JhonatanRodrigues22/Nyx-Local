# Review Checklist

Use this checklist before approving a Pull Request.

## Architecture

- [ ] The implementation follows the documented layer boundaries.
- [ ] Domain does not depend on infrastructure.
- [ ] Application does not depend on concrete providers.
- [ ] Infrastructure implements domain contracts.
- [ ] Bootstrap owns concrete wiring.

## Scope

- [ ] The PR implements only the Sprint scope.
- [ ] Out-of-scope capabilities were not added.
- [ ] No unnecessary dependencies were introduced.

## Code Quality

- [ ] Responsibilities are clear and focused.
- [ ] Naming matches existing project conventions.
- [ ] No avoidable import cycles were introduced.
- [ ] Code is simple enough for future contributors to extend.

## Tests

- [ ] Relevant tests were added or updated.
- [ ] Tests pass locally.
- [ ] Filesystem behavior uses isolated test paths.

## Documentation

- [ ] Impacted `.ai` documents were updated.
- [ ] `SPRINT_REPORT.md` was updated.
- [ ] Architectural decisions were recorded when needed.

## Delivery

- [ ] `scripts/package_project.py` was executed.
- [ ] The branch is ready for Tech Leader review.
- [ ] The PR body clearly explains what changed and why.
