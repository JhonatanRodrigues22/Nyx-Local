from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BRANCH_NAME = "sprint-02-5-core-refinement-git-flow"
COMMIT_TITLE = "refactor(core): refine request flow and add PR preparation script"
COMMIT_DESCRIPTION = """## Added

- Console interface for rendering responses
- PR preparation helper script

## Changed

- Refined Request field naming
- Refined Application handler naming
- Updated tests for the new flow
- Updated AI documentation and sprint report

## Notes

This Sprint prepares the project workflow for safer Git-based reviews before pushing changes.
"""


def run_command(command: list[str], *, check: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        capture_output=True,
        check=check,
        text=True,
    )


def has_command(command: str) -> bool:
    return shutil.which(command) is not None


def is_git_repository() -> bool:
    result = run_command(["git", "rev-parse", "--is-inside-work-tree"])
    return result.returncode == 0 and result.stdout.strip() == "true"


def get_current_branch() -> str:
    result = run_command(["git", "branch", "--show-current"], check=True)
    return result.stdout.strip()


def branch_exists(branch_name: str) -> bool:
    result = run_command(["git", "rev-parse", "--verify", branch_name])
    return result.returncode == 0


def prepare_branch(branch_name: str) -> None:
    current_branch = get_current_branch()
    print(f"Current branch: {current_branch}")

    if current_branch == branch_name:
        print(f"Already on branch: {branch_name}")
        return

    if branch_exists(branch_name):
        run_command(["git", "switch", branch_name], check=True)
        print(f"Switched to existing branch: {branch_name}")
        return

    run_command(["git", "switch", "-c", branch_name], check=True)
    print(f"Created and switched to branch: {branch_name}")


def run_tests() -> None:
    print("Running tests...")
    result = run_command([sys.executable, "-m", "pytest"])
    print(result.stdout, end="")

    if result.stderr:
        print(result.stderr, end="")

    if result.returncode != 0:
        raise RuntimeError("Tests failed. Fix the test suite before preparing the PR.")


def generate_package() -> None:
    print("Generating clean package...")
    result = run_command([sys.executable, "scripts/package_project.py"])
    print(result.stdout, end="")

    if result.stderr:
        print(result.stderr, end="")

    if result.returncode != 0:
        raise RuntimeError("Package generation failed.")


def get_changed_files() -> str:
    result = run_command(["git", "status", "--short"], check=True)
    return result.stdout.strip() or "No changed files detected."


def build_push_command(branch_name: str) -> str:
    return f"git push -u origin {branch_name}"


def build_pr_command() -> str:
    return f'gh pr create --title "{COMMIT_TITLE}" --body-file SPRINT_REPORT.md'


def print_commit_guidance(branch_name: str) -> None:
    print("\nSuggested commit title:")
    print(COMMIT_TITLE)

    print("\nSuggested commit description:")
    print(COMMIT_DESCRIPTION)

    print("Suggested commands:")
    print("git add .")
    print(f'git commit -m "{COMMIT_TITLE}"')
    print(build_push_command(branch_name))

    if has_command("gh"):
        print(build_pr_command())
    else:
        print("GitHub CLI not detected. Create the Pull Request manually after push.")

    print("\nNo push or Pull Request was executed automatically.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prepare a Sprint branch for Pull Request review.")
    parser.add_argument(
        "branch_name",
        nargs="?",
        default=DEFAULT_BRANCH_NAME,
        help="Sprint branch name to create or switch to.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if not has_command("git"):
        print("Git is not installed or is not available in PATH.")
        return 1

    if not is_git_repository():
        print("This project is not inside a Git repository.")
        print("Initialize or clone the repository before preparing a Pull Request.")
        return 1

    try:
        prepare_branch(args.branch_name)
        run_tests()
        generate_package()

        print("\nChanged files:")
        print(get_changed_files())

        print_commit_guidance(args.branch_name)
    except (RuntimeError, subprocess.CalledProcessError) as error:
        print(f"PR preparation stopped: {error}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
