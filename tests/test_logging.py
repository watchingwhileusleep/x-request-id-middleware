import logging
import pytest

from collections.abc import Generator

from x_request_id_middleware.common import set_request_id
from x_request_id_middleware.logging_config import configure_logging


@pytest.fixture(autouse=True)
def reset_logging() -> Generator[None, None, None]:
    """
    Automatically reset logging configuration before each test.

    This ensures that each test starts with a fresh logging configuration,
    avoiding any leftover configuration from previous tests.
    """
    root_logger = logging.getLogger()
    original_handlers = root_logger.handlers[:]
    original_level = root_logger.level
    original_filters = root_logger.filters[:]

    root_logger.handlers.clear()
    root_logger.filters.clear()

    yield

    root_logger.handlers = original_handlers
    root_logger.level = original_level
    root_logger.filters = original_filters


def test_logging_with_request_id_in_configure_logging(caplog):
    """
    Test that the logger includes the request ID in log messages.
    """
    configure_logging("%(asctime)s %(levelname)s [%(request_id)s] %(message)s")

    request_id = "test_request_id"
    set_request_id(request_id)

    with caplog.at_level(logging.INFO):
        logging.info("This is a test log message")

    assert any(record.request_id == request_id for record in caplog.records)


def test_logging_without_request_id_in_configure_logging(caplog):
    """
    Test that the logger includes the request ID in log messages.
    """
    configure_logging()

    request_id = "test_request_id"
    set_request_id(request_id)

    with caplog.at_level(logging.INFO):
        logging.info("This is a test log message")

    assert any(record.request_id == request_id for record in caplog.records)


def test_logging_without_configure_logging(caplog):
    """
    Test that the logger does not include request ID if configure_logging
    is not called.
    """
    with caplog.at_level(logging.INFO):
        logging.info("This is a test log message")

    assert not any(hasattr(record, "request_id") for record in caplog.records)
