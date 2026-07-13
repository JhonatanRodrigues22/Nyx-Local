"""Run the real Nyx OS PR #30 server against this Python client."""

import argparse
import os
import shutil
import subprocess
from pathlib import Path


def parse_args() -> argparse.Namespace:
    project = Path(__file__).resolve().parents[1]
    default_nyx_os = project.parents[1] / "Nyx-OS"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--nyx-os", type=Path, default=default_nyx_os)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    project = Path(__file__).resolve().parents[1]
    nyx_os = args.nyx_os.resolve()
    fixture = project / "tests" / "integration" / "nyx_os_gateway.integration.ts"
    destination = nyx_os / "apps" / "web" / "src" / "components" / "_NyxLocalIntegration.test.ts"
    jest = nyx_os / "node_modules" / ".bin" / "jest.cmd"
    python = project / ".venv" / "Scripts" / "python.exe"
    node_directory = Path("C:/Program Files/nodejs")

    if not (nyx_os / "packages" / "local-gateway").is_dir():
        raise FileNotFoundError(f"Nyx OS local-gateway package not found: {nyx_os}")
    if not jest.is_file():
        raise FileNotFoundError(f"Nyx OS Jest executable not found: {jest}")
    if not python.is_file():
        raise FileNotFoundError(f"Nyx Local virtual environment not found: {python}")
    if not (node_directory / "node.exe").is_file():
        raise FileNotFoundError(f"Node.js executable not found: {node_directory}")

    shutil.copyfile(fixture, destination)
    environment = os.environ.copy()
    environment["NYX_LOCAL_PROJECT_PATH"] = str(project)
    environment["NYX_LOCAL_PYTHON"] = str(python)
    environment["PATH"] = f"{node_directory}{os.pathsep}{environment.get('PATH', '')}"

    try:
        subprocess.run(
            [str(jest), "--runInBand", f"src/components/{destination.name}"],
            cwd=nyx_os / "apps" / "web",
            env=environment,
            check=True,
        )
    finally:
        destination.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
