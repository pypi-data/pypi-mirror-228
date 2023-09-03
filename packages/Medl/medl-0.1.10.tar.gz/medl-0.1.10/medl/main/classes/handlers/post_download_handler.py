from typing import List
from medl.common import SongData, BaseLogger, BaseOptionsManager
from medl.main.interfaces import BasePathFormatter

__all__ = ["PostDownloadHandler"]


class PostDownloadHandler:
    def __init__(
        self,
        logger: BaseLogger,
        options_manager: BaseOptionsManager,
        path_formatter: BasePathFormatter,
    ) -> None:
        self._logger = logger
        self._options = options_manager.get_options()
        self._path_formatter = path_formatter

    def exec(self, tracks: List[SongData]) -> List[SongData]:
        self._logger.debug("Post-download operation")

        if self._options.generate_m3u:
            # generate m3u file
            return tracks

        return tracks
