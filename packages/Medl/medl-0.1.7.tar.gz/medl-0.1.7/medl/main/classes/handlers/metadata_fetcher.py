from typing import List
from mumee import (
    SongMetadata,
    BaseMetadataClient,
    BaseMetadataExplorer,
    SearchMetadataCommand,
)

from medl.common import SongData, BaseOptionsManager
from medl.main.interfaces import BaseMetadataFetcherLogger

__all__ = ["MetadataFetcher"]


class MetadataFetcher:
    def __init__(
        self,
        logger: BaseMetadataFetcherLogger,
        options_manager: BaseOptionsManager,
        metadata_client: BaseMetadataClient,
        metadata_explorer: BaseMetadataExplorer,
    ) -> None:
        self._logger = logger
        self._options = options_manager.get_options()
        self._metadata_client = metadata_client
        self._metadata_explorer = metadata_explorer

    def fetch(self, query: str) -> List[SongData]:
        self._logger.start_fetching(query)

        metadata = self._metadata_client.exec(query)

        if metadata is None:
            self._logger.no_result(query)
            return []

        if isinstance(metadata, SongMetadata):  # song
            track_data = SongData.from_mumee(metadata)

            self._logger.fetched_track(track_data)
            return [track_data]
        else:  # playlist
            track_list = [SongData.from_mumee(track) for track in metadata.tracks]

            self._logger.fetched_playlist(metadata.name, len(metadata.tracks))
            return track_list

    def search(
        self,
        query: str,
        limit: int,
        sorted: bool = False,
    ) -> List[SongData]:
        command = SearchMetadataCommand(
            query=query,
            limit_per_client=limit,
            sorted=sorted,
            clients=self._options.metadata_providers,
        )
        metadatas = self._metadata_explorer.exec(command)

        if metadatas is None:
            self._logger.no_result(query)
            return []

        tracks = [SongData.from_mumee(track) for track in metadatas]
        return tracks
