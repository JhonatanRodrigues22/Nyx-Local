from nyx_local.core import Request
from nyx_local.core.bootstrap import Bootstrap


def main() -> None:
    """Run the minimal Nyx Local application flow."""
    bootstrap = Bootstrap()
    app = bootstrap.initialize()

    try:
        request = Request(message="", origin="main")
        app.run(request)
    finally:
        bootstrap.shutdown()
