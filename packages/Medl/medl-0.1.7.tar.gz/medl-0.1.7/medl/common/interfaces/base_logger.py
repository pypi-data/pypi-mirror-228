from typing import Protocol

__all__ = ["BaseLogger"]


class BaseLogger(Protocol):
    def set_level(self, log_level: int) -> None:
        ...

    def debug(self, msg: str, *args) -> None:
        ...

    def info(self, msg: str, *args) -> None:
        ...

    def warning(self, msg: str, *args) -> None:
        ...

    def error(self, msg: str, *args) -> None:
        ...

    def critical(self, msg: str, *args) -> None:
        ...
