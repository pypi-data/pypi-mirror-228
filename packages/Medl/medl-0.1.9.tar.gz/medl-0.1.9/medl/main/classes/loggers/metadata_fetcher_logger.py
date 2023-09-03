from medl.common import SongData, BaseLogger

__all__ = ["MetadataFetcherLogger"]


class MetadataFetcherLogger:
    def __init__(self, logger: BaseLogger) -> None:
        self._logger = logger

    def start_fetching(self, query: str) -> None:
        self._logger.info(f"Fetching metadata for {query}")

    def fetched_track(self, track_data: SongData) -> None:
        self._logger.info(
            f"Found metadata for {track_data.name} - {', '.join(track_data.artists)}"
        )

    def fetched_playlist(self, playlist_name: str, playlist_length: int) -> None:
        self._logger.info(f"Found playlist {playlist_name} with {playlist_length} tracks")

    def no_result(self, query: str) -> None:
        self._logger.error(f"Couldn't find metadata for query {query}")
