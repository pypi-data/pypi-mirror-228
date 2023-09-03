from typing import Protocol
from medl.common import SongData

__all__ = ["BaseMetadataEmbedderLogger"]


class BaseMetadataEmbedderLogger(Protocol):
    def start_embedding(self, track_data: SongData) -> None:
        ...

    def embedded(self, track_data: SongData) -> None:
        ...

    def error_embedding(self, track_data: SongData, path: str) -> None:
        ...
