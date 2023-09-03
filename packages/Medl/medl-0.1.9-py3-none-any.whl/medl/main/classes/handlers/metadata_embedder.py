from pathlib import Path
from typing import Optional
from yumee import BaseSongFileProvider

from medl.common import SongData
from medl.main.interfaces import BaseMetadataEmbedderLogger

__all__ = ["MetadataEmbedder"]


class MetadataEmbedder:
    def __init__(
        self,
        logger: BaseMetadataEmbedderLogger,
        song_file_provider: BaseSongFileProvider,
    ) -> None:
        self._logger = logger
        self._song_file_provider = song_file_provider

    def embed(self, track_data: SongData, path: Path, lyrics: Optional[str]) -> bool:
        self._logger.start_embedding(track_data)

        track_data.lyrics = lyrics
        metadata = track_data.to_yumee()

        song_file = self._song_file_provider.exec(path)

        if song_file is None:
            self._logger.error_embedding(track_data, str(path))
            return False
        else:
            song_file.embed(metadata)
            self._logger.embedded(track_data)
            return True
