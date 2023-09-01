from medl.common import SongData, BaseLogger

__all__ = ["LyricsFetcherLogger"]


class LyricsFetcherLogger:
    def __init__(self, logger: BaseLogger) -> None:
        self._logger = logger

    def start_fetching(self, track_data: SongData) -> None:
        self._logger.info(f"{self._log_prefix(track_data)} Fetching lyrics")

    def fetched(self, track_data: SongData) -> None:
        self._logger.debug(f"{self._log_prefix(track_data)} Fetched lyrics")

    def no_result(self, track_data: SongData) -> None:
        self._logger.warning(f"{self._log_prefix(track_data)} Lyrics not found")

    def _log_prefix(self, track_data: SongData) -> str:
        return f"[{track_data.name} - {', '.join(track_data.artists)}]"
