from medl.common import SongData, BaseLogger

__all__ = ["TrackConverterLogger"]


class TrackConverterLogger:
    def __init__(self, logger: BaseLogger) -> None:
        self._logger = logger

    def start_converting(self, track_data: SongData) -> None:
        self._logger.info(f"{self._log_prefix(track_data)} Converting track")

    def converted(self, track_data: SongData) -> None:
        self._logger.debug(f"{self._log_prefix(track_data)} Track converted")

    def error_converting(self, track_data: SongData, error_message: str) -> None:
        self._logger.error(f"{self._log_prefix(track_data)} {error_message}")

    def _log_prefix(self, track_data: SongData) -> str:
        return f"[{track_data.name} - {', '.join(track_data.artists)}]"
