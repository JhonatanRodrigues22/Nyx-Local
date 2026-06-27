from nyx_local.core import Response


class ConsoleInterface:
    """Console output boundary for rendering application responses."""

    def render(self, response: Response) -> None:
        print(response)
