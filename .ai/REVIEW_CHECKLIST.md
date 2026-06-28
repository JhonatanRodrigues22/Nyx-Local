# Review Checklist

Use this checklist before approving a Pull Request.

## Capability

- [ ] The PR states the capability added.
- [ ] `SPRINT_REPORT.md` includes `Capability Added`.
- [ ] The implementation matches the Sprint acceptance criteria.

## Architecture

- [ ] Layer boundaries from `ARCHITECTURE_GUIDE.md` are respected.
- [ ] Domain does not depend on Infrastructure.
- [ ] Application does not depend on concrete providers.
- [ ] Infrastructure implements Domain contracts.
- [ ] Bootstrap owns concrete wiring.

## Scope

- [ ] The PR implements only the approved scope.
- [ ] Out-of-scope capabilities were not added.
- [ ] No unnecessary dependencies were introduced.

## Code Quality

- [ ] Responsibilities are clear.
- [ ] Naming follows `CODE_STYLE.md`.
- [ ] No avoidable import cycles were introduced.
- [ ] The code remains easy to extend.

## Tests

- [ ] Relevant tests were added or updated.
- [ ] Tests pass locally.
- [ ] Filesystem behavior uses isolated test paths.

## Documentation

- [ ] Impacted `.ai` documents were updated.
- [ ] Cross-references are clear.
- [ ] No conflicting duplicate guidance was introduced.
- [ ] Architectural decisions were recorded when needed.

## Delivery

- [ ] `scripts/package_project.py` was executed.
- [ ] The Pull Request body explains what changed and why.
- [ ] The branch is ready for Tech Leader review.
