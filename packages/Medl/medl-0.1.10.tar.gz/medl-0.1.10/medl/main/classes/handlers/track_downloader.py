from typing import Optional
from medl.common import SongData, MedlException
from medl.main.data import DownloadInfo
from medl.main.interfaces import (
    BaseTrackDownloaderLogger,
    BaseDownloader,
)

__all__ = ["TrackDownloader"]


class TrackDownloader:
    def __init__(
        self,
        logger: BaseTrackDownloaderLogger,
        downloader: BaseDownloader,
    ) -> None:
        self._logger = logger
        self._downloader = downloader

    def download(self, track_data: SongData, download_url: str) -> Optional[DownloadInfo]:
        self._logger.start_downloading(track_data, download_url)

        try:
            download_info = self._downloader.download(download_url)

            self._logger.downloaded(track_data)
            return download_info
        except MedlException as ex:
            self._logger.error_downloading(track_data, str(ex))
            return None
