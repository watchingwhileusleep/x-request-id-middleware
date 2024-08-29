from typing import Callable

from django.http import HttpRequest
from django.http import HttpResponse

from .common import generate_x_request_id
from .common import get_x_request_id
from .common import set_x_request_id
from .constants import X_REQUEST_ID_HEADER


class XRequestIDMiddleware:
    """
    Middleware for Django that generates a x-request-ID and ensures it's
    available throughout the request lifecycle.
    """

    def __init__(
        self,
        get_response: Callable[[HttpRequest], HttpResponse],
    ) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """
        Process the incoming request to extract or generate a x-request-ID
        and attach it to the request and response.

        :param request: Django's HttpRequest object.
        :return: HttpResponse object with the x-request-ID attached.
        """
        x_request_id: str = request.headers.get(
            X_REQUEST_ID_HEADER,
            generate_x_request_id(),
        )
        set_x_request_id(x_request_id)

        # Process the request and get the response
        response = self.get_response(request)

        # Attach the x-request-ID to the request's
        # metadata and response headers
        request.META[X_REQUEST_ID_HEADER] = get_x_request_id()
        response[X_REQUEST_ID_HEADER] = get_x_request_id()

        return response
