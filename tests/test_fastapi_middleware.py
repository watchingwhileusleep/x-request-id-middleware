import pytest

from fastapi import FastAPI
from fastapi.testclient import TestClient
from starlette.responses import Response

from x_request_id_middleware.common import get_request_id
from x_request_id_middleware.fastapi_middleware import (
    FastAPIXRequestIDMiddleware,
)

app = FastAPI()
app.add_middleware(FastAPIXRequestIDMiddleware)


@app.get("/")
async def read_root():
    """
    GET request handler for the root path ('/').

    This function returns the current request ID, which was
    either generated or extracted from the request headers.

    :return: A dictionary containing the request ID.
    """
    return {"request_id": get_request_id()}


@pytest.fixture
def client() -> TestClient:
    """
    Fixture to initialize and return a TestClient instance for testing
    the FastAPI app.

    The TestClient simulates requests to the FastAPI app, allowing testing
    of the middleware and route handling logic without running
    an actual server.

    :return: A TestClient instance for making requests to the app.
    """
    return TestClient(app)


def test_fastapi_middleware(client: TestClient) -> None:
    """
    Test that the FastAPI middleware correctly sets the request ID in the
    request and response.
    """
    response: Response = client.get("/")

    assert response.status_code == 200
    assert "X-Request-ID" in response.headers
    assert get_request_id() is not None
