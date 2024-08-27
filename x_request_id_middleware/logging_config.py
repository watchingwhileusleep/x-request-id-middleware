import logging
import re

from x_request_id_middleware.common import get_request_id


class OptionalXRequestIDFormatter(logging.Formatter):
    """
    Custom formatter that optionally includes `request_id` in the log output.
    """
    def __init__(self, fmt=None) -> None:
        """
        Initializes the formatter, setting up two different
        formats: one that includes the request_id and one that does not.
        These formats are derived from the provided fmt parameter.

        :param fmt: A format string for logging, which may be None.
            If None, default formats will be used.
        """
        super().__init__(fmt)
        self.fmt_with_request_id = self._fmt_with_request_id(fmt)
        self.fmt_without_request_id = self._fmt_without_request_id(fmt)

    def format(self, record: logging.LogRecord) -> str:
        """
        Overrides the base format method to decide whether to include
        request_id in the log message. If the record has a request_id
        attribute, it uses the format with the request_id; otherwise,
        it uses the format without the request_id.

        :param record: A logging.LogRecord object representing the log event.
        :return: The formatted log message as a string.
        """
        if hasattr(record, "request_id"):
            self._style._fmt = self.fmt_with_request_id
        else:
            self._style._fmt = self.fmt_without_request_id

        return super().format(record)

    def _fmt_with_request_id(self, fmt: str | None) -> str:
        """
        Helper method to construct a log format string that includes
        the request_id. If the provided fmt is not None, it appends
        the request_id field to it. Otherwise, it returns a default format
        with the request_id included.

        :param fmt: A format string for logging or None.
        :return: A format string that includes request_id.
        """
        if fmt:
            if "request_id" in fmt:
                fmt = re.sub(r"\[\s*%\(\w+\)s\s*\]", "[%(request_id)s]", fmt)
            else:
                fmt = fmt + " [%(request_id)s]"
        else:
            fmt = (
                "%(asctime)s %(levelname)s %(name)s - %(message)s "
                "[%(request_id)s]"
            )
        return fmt

    def _fmt_without_request_id(self, fmt: str | None) -> str:
        """
        Helper method to construct a log format string that does not include
        the request_id. If the provided fmt is None, it returns a default
        log format. Otherwise, it returns the provided fmt.

        :param fmt: A format string for logging or None.
        :return: A format string without request_id.
        """
        if fmt:
            fmt = re.sub(r"\[\s*%\(\w+\)s\s*\]","", fmt).strip()
            fmt = re.sub(r"\s+"," ", fmt)
        else:
            fmt = (
                "%(asctime)s %(levelname)s %(name)s - %(message)s"
            )
        return fmt


def configure_logging(str_format: str = None) -> None:
    """
    Configures logging to include request ID in log messages.

    :param str_format: Formatter string to use in log messages.
    """
    class XRequestIDLogFilter(logging.Filter):
        """
        Logging filter to inject the request ID into log records.
        """
        def filter(self, record: logging.LogRecord) -> bool:
            record.request_id = get_request_id() or "unknown"
            return True

    formatter = OptionalXRequestIDFormatter(str_format)

    logger = logging.getLogger()
    logger.addFilter(XRequestIDLogFilter())

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
