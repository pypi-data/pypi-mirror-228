from medl.common import SongData, BaseLogger

__all__ = ["MetadataEmbedderLogger"]


class MetadataEmbedderLogger:
    def __init__(self, logger: BaseLogger) -> None:
        self._logger = logger

    def start_embedding(self, track_data: SongData) -> None:
        self._logger.info(f"{self._log_prefix(track_data)} Embedding metadata")

    def embedded(self, track_data: SongData) -> None:
        self._logger.debug(f"{self._log_prefix(track_data)} Metadata embedded")
        ...

    def error_embedding(self, track_data: SongData, path: str) -> None:
        self._logger.error(
            f"{self._log_prefix(track_data)} Format isn't supported or couldn't find path {path}"
        )

    def _log_prefix(self, track_data: SongData) -> str:
        return f"[{track_data.name} - {', '.join(track_data.artists)}]"
