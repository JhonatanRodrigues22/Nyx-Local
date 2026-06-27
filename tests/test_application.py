from nyx_local.application import Application
from nyx_local.core import Request, Response


def test_application_handles_request_with_response_model() -> None:
    application = Application()
    request = Request(message="hello", origin="test")

    response = application.handle(request)

    assert isinstance(response, Response)
    assert response.success is True
    assert response.message == "Request handled successfully."
    assert response.metadata["request_origin"] == "test"
