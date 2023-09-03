from typing import Protocol, List
from medl.common import SongData

__all__ = ["BasePostDownloadHandler"]


class BasePostDownloadHandler(Protocol):
    def exec(self, tracks: List[SongData]) -> List[SongData]:
        ...
