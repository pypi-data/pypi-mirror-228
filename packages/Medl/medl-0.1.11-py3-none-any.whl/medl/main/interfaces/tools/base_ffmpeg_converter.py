from pathlib import Path
from typing import Protocol

__all__ = ["BaseFfmpegConverter"]


class BaseFfmpegConverter(Protocol):
    def convert(self, input_file: Path, output_file: Path) -> None:
        ...
