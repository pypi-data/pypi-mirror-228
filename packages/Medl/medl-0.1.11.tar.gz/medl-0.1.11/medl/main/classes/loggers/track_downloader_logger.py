from medl.common import SongData, BaseLogger

__all__ = ["TrackDownloaderLogger"]


class TrackDownloaderLogger:
    def __init__(self, logger: BaseLogger) -> None:
        self._logger = logger

    def start_downloading(self, track_data: SongData, download_url: str) -> None:
        self._logger.info(
            f"{self._log_prefix(track_data)} Downloading with url {download_url}"
        )

    def downloaded(self, track_data: SongData) -> None:
        self._logger.debug(f"{self._log_prefix(track_data)} Downloaded")

    def error_downloading(self, track_data: SongData, error_message: str) -> None:
        self._logger.error(f"{self._log_prefix(track_data)} Download failed")

    def _log_prefix(self, track_data: SongData) -> str:
        return f"[{track_data.name} - {', '.join(track_data.artists)}]"
