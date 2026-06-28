from __future__ import annotations

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DIST_DIR = PROJECT_ROOT / "dist"
PACKAGE_PATH = DIST_DIR / "nyx_local_project.zip"

INCLUDE_PATHS = [
    "src",
    "tests",
    "docs",
    "config",
    "scripts",
    "data",
    ".ai",
    "README.md",
    "DEVELOPMENT_RULES.md",
    "requirements.txt",
    "requirements-dev.txt",
    "pyproject.toml",
    ".gitignore",
    "main.py",
    "SPRINT_REPORT.md",
]

IGNORED_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    ".mypy_cache",
    "dist",
    "build",
    "logs",
}

IGNORED_SUFFIXES = {".pyc", ".log", ".zip"}


def should_ignore(path: Path) -> bool:
    relative_parts = path.relative_to(PROJECT_ROOT).parts

    if any(part in IGNORED_DIRS for part in relative_parts):
        return True

    if path.suffix in IGNORED_SUFFIXES:
        return True

    return any(part.endswith(".egg-info") for part in relative_parts)


def iter_package_files() -> list[Path]:
    package_files: list[Path] = []

    for include_path in INCLUDE_PATHS:
        path = PROJECT_ROOT / include_path

        if not path.exists():
            continue

        if path.is_file():
            if not should_ignore(path):
                package_files.append(path)
            continue

        for file_path in path.rglob("*"):
            if file_path.is_file() and not should_ignore(file_path):
                package_files.append(file_path)

    return sorted(package_files)


def main() -> None:
    DIST_DIR.mkdir(exist_ok=True)

    with ZipFile(PACKAGE_PATH, "w", ZIP_DEFLATED) as package:
        for file_path in iter_package_files():
            package.write(file_path, file_path.relative_to(PROJECT_ROOT))

    print(f"Package created: {PACKAGE_PATH}")


if __name__ == "__main__":
    main()
