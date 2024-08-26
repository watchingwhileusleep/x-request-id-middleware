from typing import Awaitable
from typing import Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from .common import generate_request_id
from .common import get_request_id
from .common import set_request_id
from .constants import REQUEST_ID_HEADER


class FastAPIXRequestIDMiddleware(BaseHTTPMiddleware):
    """
    Middleware for FastApi that generates or retrieves a request ID and
    ensures it is passed in the response headers.
    """

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        """
        Middleware logic to handle the generation or retrieval of request ID
        and propagate it through the FastAPI request-response cycle.

        :param request: FastAPI's Request object.
        :param call_next: Next middleware or handler in the request chain.
        :return: Response object with the request ID attached to headers.
        """
        request_id: str = request.headers.get(
            REQUEST_ID_HEADER,
            generate_request_id(),
        )
        set_request_id(request_id)

        # Call the next middleware or handler
        response: Response = await call_next(request)

        # Attach th request ID to the response
        response.headers[REQUEST_ID_HEADER] = get_request_id()

        return response
