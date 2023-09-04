from typing import List, Protocol, Union

from medl.common import SongData, PlaylistData

__all__ = ["BaseMetadataFetcher"]


class BaseMetadataFetcher(Protocol):
    def search(
        self,
        query: str,
        limit: int,
        sorted: bool = False,
    ) -> List[SongData]:
        ...

    def fetch(self, query: str) -> Union[SongData, PlaylistData, None]:
        ...
