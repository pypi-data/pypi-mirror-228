from typing import List

from medl.common import BaseLogger, SongData, BaseInitializer
from medl.main.interfaces import (
    BaseParallelizer,
    BaseMetadataFetcher,
    BaseDownloadUrlFinder,
    BaseLyricsFetcher,
    BaseMetadataEmbedder,
    BaseTrackConverter,
    BaseTrackDownloader,
    BasePreDownloadHandler,
    BasePostDownloadHandler,
)

__all__ = ["MusicToolbox"]


class MusicToolbox:
    def __init__(
        self,
        logger: BaseLogger,
        parallelizer: BaseParallelizer,
        pre_download_handler: BasePreDownloadHandler,
        metadata_fetcher: BaseMetadataFetcher,
        download_url_finder: BaseDownloadUrlFinder,
        lyrics_fetcher: BaseLyricsFetcher,
        track_downloader: BaseTrackDownloader,
        track_converter: BaseTrackConverter,
        metadata_embedder: BaseMetadataEmbedder,
        post_download_handler: BasePostDownloadHandler,
        initializer: BaseInitializer,
    ) -> None:
        self._logger = logger
        self._parallelizer = parallelizer
        self._initializer = initializer
        self._is_initialized = False

        self._pre_download_handler = pre_download_handler
        self._metadata_fetcher = metadata_fetcher
        self._download_url_finder = download_url_finder
        self._lyrics_fetcher = lyrics_fetcher
        self._track_downloader = track_downloader
        self._track_converter = track_converter
        self._metadata_embedder = metadata_embedder
        self._post_download_handler = post_download_handler
        

    def search_and_download(self, queries: List[str]) -> None:
        self._check_init()
        self._logger.info("Execution started")

        metadata_results: List[List[SongData]] = self._parallelizer.run_in_parallel(
            self.fetch, queries
        )
        tracks = [track for track_list in metadata_results for track in track_list]

        self.download(tracks)

    def search(
        self,
        query: str,
        limit: int,
        sorted: bool = False,
    ) -> List[SongData]:
        self._check_init()
        results = self._metadata_fetcher.search(query, limit, sorted)
        return results

    def fetch(self, query: str) -> List[SongData]:
        self._check_init()
        results = self._metadata_fetcher.fetch(query)
        return results

    def download(self, tracks: List[SongData]) -> None:
        self._check_init()
        tracks = self._pre_download_handler.exec(tracks)

        self._parallelizer.run_in_parallel(self._download_track, tracks)

        self._post_download_handler.exec(tracks)

    def _download_track(self, track_data: SongData) -> None:
        download_url = self._download_url_finder.search(track_data)
        if download_url is None:
            return

        download_info = self._track_downloader.download(track_data, download_url)
        if download_info is None:
            return

        new_path = self._track_converter.convert(track_data, download_info)
        if new_path is None:
            return

        lyrics = self._lyrics_fetcher.fetch(track_data)
        embedded = self._metadata_embedder.embed(track_data, new_path, lyrics)

        self._logger.info(
            f"[{track_data.name} - {', '.join(track_data.artists)}] Completed"
        )
        
    def _check_init(self):
        if not self._is_initialized:
            self._initializer.exec(None)
            self._is_initialized = True
