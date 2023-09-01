from typing import Optional
from lyrics_client import BaseLyricsClient, FetchLyricsCommand
from medl.common import SongData, BaseOptionsManager
from medl.main.interfaces import BaseLyricsFetcherLogger

__all__ = ["LyricsFetcher"]


class LyricsFetcher:
    def __init__(
        self,
        logger: BaseLyricsFetcherLogger,
        options_manager: BaseOptionsManager,
        lyrics_client: BaseLyricsClient,
    ) -> None:
        self._logger = logger
        self._options = options_manager.get_options()
        self._lyrics_client = lyrics_client

    def fetch(self, track_data: SongData) -> Optional[str]:
        self._logger.start_fetching(track_data)

        lyrics_command = FetchLyricsCommand(
            track_data.name,
            ", ".join(track_data.artists),
            self._options.lyrics_providers,
        )
        lyrics_results = self._lyrics_client.exec(lyrics_command)

        if not lyrics_results:
            self._logger.no_result(track_data)
            return None
        else:
            self._logger.fetched(track_data)
            return [r for r in lyrics_results if r.lyrics is not None][0].lyrics
