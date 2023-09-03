from typing import Protocol
from medl.common import SongData

__all__ = ["BaseTrackDownloaderLogger"]


class BaseTrackDownloaderLogger(Protocol):
    def start_downloading(self, track_data: SongData, download_url: str) -> None:
        ...

    def downloaded(self, track_data: SongData) -> None:
        ...

    def error_downloading(self, track_data: SongData, error_message: str) -> None:
        ...
