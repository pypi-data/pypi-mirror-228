from dataclasses import dataclass
from typing import List
from mumee import (
    PlaylistMetadata as MumeePlaylistMetadata,
)
from .song_data import SongData

__all__ = ["PlaylistData"]


@dataclass
class PlaylistData:
    name: str
    description: str
    author: str
    tracks: List[SongData]

    @classmethod
    def from_mumee(cls, metadata: MumeePlaylistMetadata) -> "PlaylistData":
        data = PlaylistData(
            name=metadata.name,
            description=metadata.description,
            author=metadata.author,
            tracks=[SongData.from_mumee(t) for t in metadata.tracks],
        )

        return data
