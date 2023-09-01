import logging
import rich

from rich.logging import RichHandler
from rich.theme import Theme
from rich.traceback import install

from medl.common.classes import LogFormatter

__all__ = ["Logger"]


class Logger:
    THEME = Theme(
        {
            "bar.back": "grey23",
            "bar.complete": "rgb(165,66,129)",
            "bar.finished": "rgb(114,156,31)",
            "bar.pulse": "rgb(165,66,129)",
            "general": "green",
            "nonimportant": "rgb(40,100,40)",
            "progress.data.speed": "red",
            "progress.description": "none",
            "progress.download": "green",
            "progress.filesize": "green",
            "progress.filesize.total": "green",
            "progress.percentage": "green",
            "progress.remaining": "rgb(40,100,40)",
            "logging.level.debug": "blue",
            "logging.level.info": "green",
            "logging.level.warning": "yellow",
            "logging.level.error": "red",
            "logging.level.critical": "bold red",
        }
    )

    def __init__(self, formatter: LogFormatter) -> None:
        self._logger = logging.getLogger("medl")
        self._formatter = formatter

        self._console = rich.get_console()
        self._console.push_theme(self.THEME)

        self._handler = None

        self.set_level(logging.DEBUG)

    def set_level(self, log_level: int) -> None:
        if self._logger.level == log_level:
            return None

        self._logger.setLevel(log_level)

        if self._handler is not None:
            self._logger.removeHandler(self._handler)

        self._handler = self._init_handler(log_level)
        self._logger.addHandler(self._handler)

        install(show_locals=False, extra_lines=1, console=self._console)

    def _init_handler(self, log_level: int) -> RichHandler:
        is_debug = log_level == logging.DEBUG

        handler = RichHandler(
            show_time=is_debug,
            log_time_format="[%X]",
            omit_repeated_times=False,
            console=self._console,
            level=log_level,
            markup=True,
            show_path=is_debug,
            show_level=is_debug,
            rich_tracebacks=True,
        )
        handler.setFormatter(self._formatter)

        return handler

    def debug(self, msg: str, *args) -> None:
        self._logger.debug(msg, *args)

    def info(self, msg: str, *args) -> None:
        self._logger.info(msg, *args)

    def warning(self, msg: str, *args) -> None:
        self._logger.warning(msg, *args)

    def error(self, msg: str, *args) -> None:
        self._logger.error(msg, *args)

    def critical(self, msg: str, *args) -> None:
        self._logger.critical(msg, *args)
