from typing import Protocol
from medl.common import SongData

__all__ = ["BaseMetadataFetcherLogger"]


class BaseMetadataFetcherLogger(Protocol):
    def start_fetching(self, query: str) -> None:
        ...

    def fetched_track(self, track_data: SongData) -> None:
        ...

    def fetched_playlist(self, playlist_name: str, playlist_length: int) -> None:
        ...

    def no_result(self, query: str) -> None:
        ...
