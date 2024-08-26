from typing import Callable
from django.http import HttpRequest
from django.http import HttpResponse

from .common import get_request_id, generate_request_id
from .common import set_request_id
from .constants import REQUEST_ID_HEADER


class XRequestIDMiddleware:
    """
    Middleware for Django that generates a request ID and ensures it's
    available throughout the request lifecycle.
    """

    def __init__(
        self,
        get_response: Callable[[HttpRequest], HttpResponse],
    ) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """
        Process the incoming request to extract or generate a request ID
        and attach it to the request and response.

        :param request: Django's HttpRequest object.
        :return: HttpResponse object with the request ID attached.
        """
        request_id: str = request.headers.get(
            REQUEST_ID_HEADER,
            generate_request_id(),
        )
        set_request_id(request_id)

        # Process the request and get the response
        response = self.get_response(request)

        # Attach the request ID to the request's metadata and response headers
        request.META[REQUEST_ID_HEADER] = get_request_id()
        response[REQUEST_ID_HEADER] = get_request_id()

        return response
