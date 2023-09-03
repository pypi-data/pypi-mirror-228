from typing import Protocol
from pathlib import Path
from medl.common import SongData

__all__ = ["BasePathFormatter"]


class BasePathFormatter(Protocol):
    def format(self, track_data: SongData) -> Path:
        ...
