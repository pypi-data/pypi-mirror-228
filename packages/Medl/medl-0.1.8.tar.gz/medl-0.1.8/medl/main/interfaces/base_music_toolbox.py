from typing import List, Protocol

from medl.common import SongData

__all__ = ["BaseMusicToolbox"]


class BaseMusicToolbox(Protocol):
    def search_and_download(self, queries: List[str]) -> None:
        ...

    def search(
        self,
        query: str,
        limit: int,
        sorted: bool = False,
    ) -> List[SongData]:
        ...

    def fetch(self, query: str) -> List[SongData]:
        ...

    def download(self, tracks: List[SongData]) -> None:
        ...
