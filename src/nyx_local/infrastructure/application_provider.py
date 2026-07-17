from __future__ import annotations

import subprocess

from nyx_local.domain.applications import ApplicationOpenFailure, ApplicationOpenSpec


class SubprocessApplicationProvider:
    """Open allowlisted applications without shell expansion or free arguments."""

    def open_application(self, spec: ApplicationOpenSpec) -> None:
        try:
            subprocess.Popen(
                [spec.command],
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                shell=False,
                close_fds=True,
            )
        except OSError as error:
            raise ApplicationOpenFailure from error
