from typing import Any

from nyx_local.core import Response
from nyx_local.interfaces import ConsoleInterface


def test_console_interface_renders_response(capsys: Any) -> None:
    console = ConsoleInterface()
    response = Response(success=True, message="ok")

    console.render(response)

    captured = capsys.readouterr()
    assert "Response(success=True, message='ok'" in captured.out
