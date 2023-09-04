from typing import Protocol
from medl.common import SongData

__all__ = ["BaseDownloadUrlFinderLogger"]


class BaseDownloadUrlFinderLogger(Protocol):
    def start_searching(self, track_data: SongData) -> None:
        ...

    def found(self, track_data: SongData) -> None:
        ...

    def no_result(self, track_data: SongData) -> None:
        ...
