import logging

from x_request_id_middleware.common import set_request_id, configure_logging


def test_logging_with_reqeust_id(caplog):
    """
    Test that the logger includes the request ID in log messages.
    """
    configure_logging()

    request_id = "test_request_id"
    set_request_id(request_id)

    with caplog.at_level(logging.INFO):
        logging.info("This is a test log message")

    assert any(record.request_id == request_id for record in caplog.records)
