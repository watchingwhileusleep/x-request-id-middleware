import logging
import uuid
import sentry_sdk

from contextvars import ContextVar
from typing import Optional

# Context variable to store request ID
request_id_context: ContextVar[Optional[str]] = ContextVar(
    "request_id",
    default=None,
)


def get_request_id() -> Optional[str]:
    """
    Retrieve the current request ID from the context.

    :return: The current request ID if it exists, otherwise None.
    """
    return request_id_context.get()


def set_request_id(request_id: str) -> None:
    """
    Set the current request ID in the context and add to Sentry.

    :param request_id: The request ID to set.
    """
    request_id_context.set(request_id)
    _add_request_id_to_sentry(request_id)


def generate_request_id() -> str:
    """
    Generates a new UUID as a request ID.

    :return: The generated request ID.
    """
    return str(uuid.uuid4())


def _add_request_id_to_sentry(request_id: str) -> None:
    """
    Add request ID to the Sentry context if Sentry is initialized.

    :param request_id: The request ID to add to Sentry's context.
    """
    if sentry_sdk.Hub.current.client:
        with sentry_sdk.configure_scope() as scope:
            scope.set_tag("request_id", request_id)


def configure_logging() -> None:
    """
    Configures logging to include request ID in log messages.
    """
    class RequestIDLogFilter(logging.Filter):
        """
        Logging filter to inject the request ID into log records.
        """
        def filter(self, record: logging.LogRecord) -> bool:
            record.request_id = get_request_id() or "unknown"
            return True

    logger = logging.getLogger()
    logger.addFilter(RequestIDLogFilter())

    for handler in logger.handlers:
        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s %(levelname)s [%(request_id)s] %(message)s"
            )
        )
