from pathlib import Path
from typing import Optional, Protocol
from medl.common import SongData
from medl.main.data import DownloadInfo

__all__ = ["BaseTrackConverter"]


class BaseTrackConverter(Protocol):
    def convert(self, track_data: SongData, download_info: DownloadInfo) -> Optional[Path]:
        ...
