from collections.abc import Awaitable
from typing import Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from .common import generate_x_request_id
from .common import get_x_request_id
from .common import set_x_request_id
from .constants import X_REQUEST_ID_HEADER


class FastAPIXRequestIDMiddleware(BaseHTTPMiddleware):
    """
    Middleware for FastApi that generates or retrieves a x-request-ID and
    ensures it is passed in the response headers.
    """

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        """
        Middleware logic to handle the generation or retrieval of x-request-ID
        and propagate it through the FastAPI request-response cycle.

        :param request: FastAPI's Request object.
        :param call_next: Next middleware or handler in the request chain.
        :return: Response object with the x-request-ID attached to headers.
        """
        x_request_id: str = request.headers.get(
            X_REQUEST_ID_HEADER,
            generate_x_request_id(),
        )
        set_x_request_id(x_request_id)

        # Call the next middleware or handler
        response: Response = await call_next(request)

        # Attach th x-request-ID to the response
        response.headers[X_REQUEST_ID_HEADER] = get_x_request_id()

        return response
