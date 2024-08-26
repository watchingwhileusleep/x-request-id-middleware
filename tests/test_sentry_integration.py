import pytest

from sentry_sdk import Hub

from x_request_id_middleware.common import set_request_id


@pytest.fixture(autouse=True)
def sentry_init(monkeypatch):
    """
    Initialize Sentry.
    """
    monkeypatch.setenv(
        "SENTRY_DSN",
        "http://public_key@example.com/123",
    )
    import sentry_sdk
    sentry_sdk.init(dsn="http://public_key@example.com/123")
    yield
    sentry_sdk.Hub.main.bind_client(None)


def test_sentry_request_id_integration():
    """
    Test that Sentry integration correctly sets the request ID
    in the Sentry scope.
    """
    request_id = "test-request-id"
    set_request_id(request_id)

    scope = Hub.current.scope
    assert scope._tags.get("request_id") == request_id
