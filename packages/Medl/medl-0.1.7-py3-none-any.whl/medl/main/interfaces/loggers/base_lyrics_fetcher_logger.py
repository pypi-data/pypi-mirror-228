from typing import Protocol
from medl.common import SongData

__all__ = ["BaseLyricsFetcherLogger"]


class BaseLyricsFetcherLogger(Protocol):
    def start_fetching(self, track_data: SongData) -> None:
        ...

    def fetched(self, track_data: SongData) -> None:
        ...

    def no_result(self, track_data: SongData) -> None:
        ...
