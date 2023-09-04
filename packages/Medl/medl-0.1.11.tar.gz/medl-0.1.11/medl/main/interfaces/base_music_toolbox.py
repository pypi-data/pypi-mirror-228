from pathlib import Path
from typing import List, Protocol, Union

from medl.common import SongData, PlaylistData

__all__ = ["BaseMusicToolbox"]


class BaseMusicToolbox(Protocol):
    def search_and_download(self, queries: List[str]) -> List[Path]:
        ...

    def search(
        self,
        query: str,
        limit: int,
        sorted: bool = False,
    ) -> List[SongData]:
        ...

    def fetch(self, query: str) -> Union[SongData, PlaylistData, None]:
        ...

    def download(self, tracks: List[SongData]) -> List[Path]:
        ...
