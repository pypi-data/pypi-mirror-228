from typing import Optional, Protocol
from medl.common import SongData

__all__ = ["BaseLyricsFetcher"]


class BaseLyricsFetcher(Protocol):
    def fetch(self, track_data: SongData) -> Optional[str]:
        ...
