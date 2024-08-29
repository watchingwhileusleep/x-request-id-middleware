import logging
import pytest

from collections.abc import Generator

from x_request_id_middleware.common import set_x_request_id
from x_request_id_middleware.logging_config import XRequestIDConfigLogging


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


def test_logging_with_x_request_id_in_configure_logging(caplog):
    """
    Test that the logger includes the x-request-ID in log messages.
    """
    x_request_id_settings = XRequestIDConfigLogging(
        "%(asctime)s %(levelname)s [%(x_request_id)s] %(message)s"
    )

    logger = logging.getLogger(__name__)
    x_request_id_settings.configure_logging(logger)

    x_request_id = "test_x_request_id"
    set_x_request_id(x_request_id)

    with caplog.at_level(logging.INFO):
        logger.info("This is a test log message")

    assert any(
        record.x_request_id == x_request_id for record in caplog.records
    )


def test_logging_without_x_request_id_in_configure_logging(caplog):
    """
    Test that the logger includes the x-request-ID in log messages.
    """
    x_request_id_settings = XRequestIDConfigLogging()

    logger = logging.getLogger(__name__)
    x_request_id_settings.configure_logging(logger)

    x_request_id = "test_x_request_id"
    set_x_request_id(x_request_id)

    with caplog.at_level(logging.INFO):
        logger.info("This is a test log message")

    assert any(
        record.x_request_id == x_request_id for record in caplog.records
    )


def test_logging_without_configure_logging(caplog):
    """
    Test that the logger does not include x-request-ID if configure_logging
    is not called.
    """
    with caplog.at_level(logging.INFO):
        logging.info("This is a test log message")

    assert not any(
        hasattr(record, "x_request_id") for record in caplog.records
    )
