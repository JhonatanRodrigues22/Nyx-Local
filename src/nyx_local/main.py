from nyx_local.core import Request
from nyx_local.core.app import App
from nyx_local.interfaces import ConsoleInterface


def main() -> None:
    """Run the minimal Nyx Local application flow."""
    app = App()
    console = ConsoleInterface()
    request = Request(message="", origin="main")
    response = app.run(request)

    console.render(response)
