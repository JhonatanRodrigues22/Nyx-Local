from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(slots=True, frozen=True)
class ApplicationOpenSpec:
    """Hardcoded application mapping approved for local opening."""

    symbolic_name: str
    command: str


class ApplicationOpenFailure(Exception):
    """Raised when an approved application cannot be opened."""


class ApplicationProvider(Protocol):
    """Open hardcoded application specs without accepting arbitrary commands."""

    def open_application(self, spec: ApplicationOpenSpec) -> None:
        """Open the application described by an allowlisted spec."""


APPLICATION_ALLOWLIST: dict[str, ApplicationOpenSpec] = {
    "vscode": ApplicationOpenSpec(symbolic_name="vscode", command="code"),
    "file-explorer": ApplicationOpenSpec(
        symbolic_name="file-explorer",
        command="explorer.exe",
    ),
    "notepad": ApplicationOpenSpec(symbolic_name="notepad", command="notepad.exe"),
}
