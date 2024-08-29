import uuid
import sentry_sdk

from contextvars import ContextVar
from typing import Optional

# Context variable to store x-request-ID
x_request_id_context: ContextVar[Optional[str]] = ContextVar(
    "x_request_id",
    default=None,
)


def get_x_request_id() -> Optional[str]:
    """
    Retrieve the current x-request-ID from the context.

    :return: The current x-request-ID if it exists, otherwise None.
    """
    return x_request_id_context.get()


def set_x_request_id(x_request_id: str) -> None:
    """
    Set the current x-request-ID in the context and add to Sentry.

    :param x_request_id: The x-request-ID to set.
    """
    x_request_id_context.set(x_request_id)
    _add_x_request_id_to_sentry(x_request_id)


def generate_x_request_id() -> str:
    """
    Generates a new UUID as a x-request-ID.

    :return: The generated x-request-ID.
    """
    return str(uuid.uuid4())


def _add_x_request_id_to_sentry(x_request_id: str) -> None:
    """
    Add x-request-ID to the Sentry context if Sentry is initialized.

    :param x_request_id: The x-request-ID to add to Sentry's context.
    """
    if sentry_sdk.Hub.current.client:
        with sentry_sdk.configure_scope() as scope:
            scope.set_tag("x_request_id", x_request_id)
