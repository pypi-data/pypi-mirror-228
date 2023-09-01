from typing import Protocol
from medl.common import SongData

__all__ = ["BaseTrackConverterLogger"]


class BaseTrackConverterLogger(Protocol):
    def start_converting(self, track_data: SongData) -> None:
        ...

    def converted(self, track_data: SongData) -> None:
        ...

    def error_converting(self, track_data: SongData, error_message: str) -> None:
        ...
