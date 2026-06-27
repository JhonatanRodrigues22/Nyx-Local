# Workflow

Every Sprint must follow this mandatory flow:

1. Read the entire `.ai` directory.
2. Read the Sprint Prompt.
3. Implement.
4. Update documentation if necessary.
5. Generate a clean package.
6. Prepare the Git/Pull Request flow.
7. Deliver for Tech Leader review.

## Documentation Rule

After each Sprint, review the `.ai` documentation and update only the documents that actually changed.

## Git and Pull Request Rule

Every Sprint must be reviewed by the Tech Leader before push.

The Git/Pull Request preparation flow is part of the official workflow. Use `scripts/prepare_pr.py` to prepare Sprint branches, run tests, generate the clean package, inspect changed files, and receive commit and Pull Request guidance.

JJ approves push only after authorization from the Tech Leader.

Automatic push must not happen without explicit JJ confirmation.
