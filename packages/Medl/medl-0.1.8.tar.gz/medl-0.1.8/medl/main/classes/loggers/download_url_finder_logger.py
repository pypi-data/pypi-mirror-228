from medl.common import SongData, BaseLogger

__all__ = ["DownloadUrlFinderLogger"]


class DownloadUrlFinderLogger:
    def __init__(self, logger: BaseLogger) -> None:
        self._logger = logger

    def start_searching(self, track_data: SongData) -> None:
        self._logger.info(f"{self._log_prefix(track_data)} Searching for download URL")

    def found(self, track_data: SongData) -> None:
        self._logger.debug(f"{self._log_prefix(track_data)} Download URL found !")

    def no_result(self, track_data: SongData) -> None:
        self._logger.error(
            f"{self._log_prefix(track_data)} No result for download URL search !"
        )

    def _log_prefix(self, track_data: SongData) -> str:
        return f"[{track_data.name} - {', '.join(track_data.artists)}]"
