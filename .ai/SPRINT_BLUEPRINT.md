# Sprint Blueprint

Every Sprint should deliver a new capability for Nyx Local, not just add code.

## Planning Philosophy

A good Sprint is small, explicit, and reviewable. It should explain why the capability matters, where it belongs in the architecture, what is excluded, and how completion will be verified.

Avoid broad prompts that mix unrelated goals. If a feature requires multiple layers, define the intended flow between those layers.

## Required Sprint Structure

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

A short phrase that names the new capability.
```

## Implementation Principle

Start from the official `.ai` documentation, then implement the smallest clean version that satisfies the acceptance criteria.
