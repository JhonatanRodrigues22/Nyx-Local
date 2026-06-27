import sys
from pathlib import Path


def main() -> None:
    """Run the minimal Nyx Local application flow from the repository root."""
    src_path = Path(__file__).resolve().parent / "src"
    sys.path.insert(0, str(src_path))

    from nyx_local.main import main as package_main

    package_main()


if __name__ == "__main__":
    main()
