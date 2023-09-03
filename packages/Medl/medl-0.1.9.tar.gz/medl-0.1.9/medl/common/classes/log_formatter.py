import logging
from logging import LogRecord

from rich.markup import escape

__all__ = ["LogFormatter"]


class LogFormatter(logging.Formatter):
    LEVEL_TO_COLOR = {
        logging.DEBUG: "[blue]",
        logging.INFO: "[green]",
        logging.WARNING: "[yellow]",
        logging.ERROR: "[red]",
        logging.CRITICAL: "[bold red]",
    }

    def format(self, record: LogRecord) -> str:
        std_message = super().format(record)

        if record.levelno == logging.DEBUG:
            std_message = f"{record.threadName} - {std_message}"

        escaped_message = escape(std_message)
        colored_message = f"{self.LEVEL_TO_COLOR[record.levelno]}{escaped_message}"

        return colored_message
