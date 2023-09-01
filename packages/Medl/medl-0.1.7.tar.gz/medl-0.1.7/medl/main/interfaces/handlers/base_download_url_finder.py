from typing import Optional, Protocol

from medl.common import SongData

__all__ = ["BaseDownloadUrlFinder"]


class BaseDownloadUrlFinder(Protocol):
    def search(self, track_data: SongData) -> Optional[str]:
        ...
