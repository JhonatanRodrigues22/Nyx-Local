from scripts.prepare_pr import (
    COMMIT_TITLE,
    DEFAULT_BRANCH_NAME,
    build_pr_command,
    build_push_command,
)


def test_prepare_pr_builds_push_command_for_branch() -> None:
    assert (
        build_push_command(DEFAULT_BRANCH_NAME)
        == "git push -u origin sprint-02-5-core-refinement-git-flow"
    )


def test_prepare_pr_builds_github_cli_command() -> None:
    assert build_pr_command() == (
        'gh pr create --title '
        '"refactor(core): refine request flow and add PR preparation script" '
        "--body-file SPRINT_REPORT.md"
    )
    assert COMMIT_TITLE.startswith("refactor(core):")
