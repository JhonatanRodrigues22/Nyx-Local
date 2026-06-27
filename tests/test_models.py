from datetime import UTC, datetime

from nyx_local.core import Request, Response


def test_request_stores_user_message_and_optional_context() -> None:
    timestamp = datetime(2026, 6, 27, tzinfo=UTC)

    request = Request(message="hello", timestamp=timestamp, origin="test")

    assert request.message == "hello"
    assert request.timestamp == timestamp
    assert request.origin == "test"


def test_response_uses_default_empty_metadata() -> None:
    response = Response(success=True, message="ok")

    assert response.success is True
    assert response.message == "ok"
    assert response.data is None
    assert response.metadata == {}
