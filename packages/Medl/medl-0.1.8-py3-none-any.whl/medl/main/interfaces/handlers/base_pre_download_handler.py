from typing import Protocol, List
from medl.common import SongData

__all__ = ["BasePreDownloadHandler"]


class BasePreDownloadHandler(Protocol):
    def exec(self, tracks: List[SongData]) -> List[SongData]:
        ...
