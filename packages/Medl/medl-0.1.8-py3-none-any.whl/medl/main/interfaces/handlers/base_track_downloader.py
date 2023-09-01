from typing import Optional, Protocol
from medl.common import SongData
from medl.main.data import DownloadInfo

__all__ = ["BaseTrackDownloader"]


class BaseTrackDownloader(Protocol):
    def download(self, track_data: SongData, download_url: str) -> Optional[DownloadInfo]:
        ...
