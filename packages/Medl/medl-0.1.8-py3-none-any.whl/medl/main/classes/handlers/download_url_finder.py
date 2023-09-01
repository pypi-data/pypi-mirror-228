from typing import Optional
from mumee import YTMusicMetadataClient

from medl.common import SongData
from medl.main.interfaces import BaseDownloadUrlFinderLogger

__all__ = ["DownloadUrlFinder"]


class DownloadUrlFinder:
    def __init__(
        self, logger: BaseDownloadUrlFinderLogger, ytm_client: YTMusicMetadataClient
    ) -> None:
        self._logger = logger
        self._ytm_client = ytm_client

    def search(self, track_data: SongData) -> Optional[str]:
        self._logger.start_searching(track_data)

        try:
            result = self._ytm_client.search(
                f"{track_data.name} - {', '.join(track_data.artists)}", 1, True
            )[0]

            self._logger.found(track_data)
            return result.url
        except:
            self._logger.no_result(track_data)
            return None
