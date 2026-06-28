# Sprint Blueprint

Every Sprint should deliver a new capability for Nyx Local, not just add code.

Use this blueprint when preparing future Sprint prompts.

## Planning Philosophy

A good Sprint is:

- small enough to review;
- clear about its new capability;
- explicit about architecture;
- strict about what is out of scope;
- verifiable through acceptance criteria.

## Required Structure

```markdown
# Sprint N - Title

## Objective

What new capability this Sprint adds.

## Context

Why this Sprint exists and what previous work it builds on.

## Scope

What must be implemented.

## Expected Architecture

The intended layer flow and dependency boundaries.

## Acceptance Criteria

Concrete behavior that proves the Sprint is complete.

## Out of Scope

Capabilities that must not be implemented yet.

## Deliverables

Code, tests, documentation, package, branch, and Pull Request expectations.

## Sprint Milestone

A short phrase that names the capability added.
```

## Sprint Report Requirement

Every future `SPRINT_REPORT.md` must include:

```markdown
## Capability Added

Nyx Local now ...
```

This section must describe the actual capability gained by the project.

## Implementation Principle

Start from the official `.ai` documentation, then implement the smallest clean version that satisfies the acceptance criteria.
