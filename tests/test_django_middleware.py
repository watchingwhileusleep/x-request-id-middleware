import os

from django.http import HttpResponse
from django.test import RequestFactory

from x_request_id_middleware.common import get_request_id
from x_request_id_middleware.django_middleware import XRequestIDMiddleware

os.environ["DJANGO_SETTINGS_MODULE"] = "tests.test_settings"


def test_django_middleware() -> None:
    """
    Test that the Django middleware correctly sets the request ID in the
    request and response
    """
    request = RequestFactory().get("/")
    middleware = XRequestIDMiddleware(lambda req: HttpResponse())

    response: HttpResponse = middleware(request)

    assert "X-Request-ID" in response
    assert get_request_id() is not None
