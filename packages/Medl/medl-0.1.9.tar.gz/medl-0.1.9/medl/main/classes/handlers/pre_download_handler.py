from typing import List
from medl.common import SongData, BaseLogger, BaseOptionsManager
from medl.main.interfaces import BasePathFormatter

__all__ = ["PreDownloadHandler"]


class PreDownloadHandler:
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
        self._logger.debug("Pre-download operation")
        tracks_to_dl = []

        for track in tracks:
            track_path = self._path_formatter.format(track)

            if track_path.exists():
                if self._options.overwrite == "skip":
                    self._logger.info(f"Skipping {track.name} - {', '.join(track.artists)}")
                    continue
                else:
                    self._logger.warning(
                        f"Overwriting {track.name} - {', '.join(track.artists)}"
                    )

            tracks_to_dl.append(track)

        return tracks_to_dl
