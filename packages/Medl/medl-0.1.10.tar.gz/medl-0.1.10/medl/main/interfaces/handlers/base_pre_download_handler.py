from pathlib import Path
from typing import Protocol, List, Tuple
from medl.common import SongData

__all__ = ["BasePreDownloadHandler"]


class BasePreDownloadHandler(Protocol):
    def exec(self, tracks: List[SongData]) -> Tuple[List[SongData], List[Path]]:
        ...
