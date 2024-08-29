import pytest

from sentry_sdk import Hub

from x_request_id_middleware.common import set_x_request_id


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


def test_sentry_x_request_id_integration():
    """
    Test that Sentry integration correctly sets the x-request-ID
    in the Sentry scope.
    """
    x_request_id = "test-x-request-id"
    set_x_request_id(x_request_id)

    scope = Hub.current.scope
    assert scope._tags.get("x_request_id") == x_request_id
