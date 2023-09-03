from pathlib import Path
from typing import Optional, Protocol

from medl.common import SongData

__all__ = ["BaseMetadataEmbedder"]


class BaseMetadataEmbedder(Protocol):
    def embed(self, track_data: SongData, path: Path, lyrics: Optional[str]) -> bool:
        ...
