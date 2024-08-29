import logging
import re

from x_request_id_middleware.common import get_x_request_id


class OptionalXRequestIDFormatter(logging.Formatter):
    """
    Custom formatter that optionally includes `x_request_id` in the log output.
    """
    def __init__(self, fmt=None) -> None:
        """
        Initializes the formatter, setting up two different
        formats: one that includes the x_request_id and one that does not.
        These formats are derived from the provided fmt parameter.

        :param fmt: A format string for logging, which may be None.
            If None, default formats will be used.
        """
        super().__init__(fmt)
        self.fmt_with_x_request_id = self._fmt_with_x_request_id(fmt)
        self.fmt_without_x_request_id = self._fmt_without_x_request_id(fmt)

    def format(self, record: logging.LogRecord) -> str:
        """
        Overrides the base format method to decide whether to include
        x_request_id in the log message. If the record has a x_request_id
        attribute, it uses the format with the x_request_id; otherwise,
        it uses the format without the x_request_id.

        :param record: A logging.LogRecord object representing the log event.
        :return: The formatted log message as a string.
        """
        if hasattr(record, "x_request_id"):
            self._style._fmt = self.fmt_with_x_request_id
        else:
            self._style._fmt = self.fmt_without_x_request_id

        return super().format(record)

    def _fmt_with_x_request_id(self, fmt: str | None) -> str:
        """
        Helper method to construct a log format string that includes
        the x_request_id. If the provided fmt is not None, it appends
        the x_request_id field to it. Otherwise, it returns a default format
        with the x_request_id included.

        :param fmt: A format string for logging or None.
        :return: A format string that includes x_request_id.
        """
        if fmt:
            if "x_request_id" in fmt:
                fmt = re.sub(
                    r"\[\s*%\(\w+\)s\s*\]",
                    "[%(x_request_id)s]",
                    fmt,
                )
            else:
                fmt = fmt + " [%(x_request_id)s]"
        else:
            fmt = (
                "%(asctime)s %(levelname)s %(name)s - %(message)s "
                "[%(x_request_id)s]"
            )
        return fmt

    def _fmt_without_x_request_id(self, fmt: str | None) -> str:
        """
        Helper method to construct a log format string that does not include
        the x_request_id. If the provided fmt is None, it returns a default
        log format. Otherwise, it returns the provided fmt.

        :param fmt: A format string for logging or None.
        :return: A format string without x_request_id.
        """
        if fmt:
            fmt = re.sub(r"\[\s*%\(\w+\)s\s*\]", "", fmt).strip()
            fmt = re.sub(r"\s+", " ", fmt)
        else:
            fmt = (
                "%(asctime)s %(levelname)s %(name)s - %(message)s"
            )
        return fmt


class XRequestIDConfigLogging:
    def __init__(self, str_format: str = None) -> None:
        """
        Initializes the configuration for logging with optional
        x_request_id formatting.

        :param str_format: Formatter string to use in log messages.
        """
        self.formatter = OptionalXRequestIDFormatter(str_format)
        self.process()

    class XRequestIDLogFilter(logging.Filter):
        """
        Logging filter to inject the x-request-ID into log records.
        """

        def filter(self, record: logging.LogRecord) -> bool:
            record.x_request_id = get_x_request_id() or "unknown"
            return True

    def process(self) -> None:
        """
        Sets up the root logger and configures it with
        the formatter and filter.
        """
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)

        for logger_name in logging.root.manager.loggerDict:
            logger = logging.getLogger(logger_name)
            self.configure_logging(logger)

    def configure_logging(self, logger: logging.Logger) -> None:
        """
        Configures a specific logger by adding a handler and filter to it.

        :param logger: The logger to configure.
        """
        handler = logging.StreamHandler()
        handler.setFormatter(self.formatter)

        if not any(
            isinstance(h, logging.StreamHandler) for h in logger.handlers
        ):
            logger.addHandler(handler)
        logger.addFilter(XRequestIDConfigLogging.XRequestIDLogFilter())
