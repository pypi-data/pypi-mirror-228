from dataclasses import dataclass
from typing import List, Optional
from mumee import SongMetadata as MumeeSongMetadata
from yumee import SongMetadata as YumeeSongMetadata

__all__ = ["SongData"]


@dataclass
class SongData:
    name: str
    artists: List[str]
    artist: str
    genres: List[str]
    disc_number: Optional[int]
    disc_count: Optional[int]
    album_name: Optional[str]
    album_artist: Optional[str]
    duration: int
    year: Optional[int]
    date: Optional[str]
    track_number: Optional[int]
    track_count: Optional[int]
    explicit: Optional[bool]
    cover_url: Optional[str]
    is_song: bool
    id: str
    url: str
    lyrics: Optional[str]

    @classmethod
    def from_mumee(cls, metadata: MumeeSongMetadata) -> "SongData":
        data = SongData(
            name=metadata.name,
            artists=metadata.artists,
            artist=metadata.artist,
            genres=metadata.genres,
            disc_number=metadata.disc_number,
            disc_count=metadata.disc_count,
            album_name=metadata.album_name,
            album_artist=metadata.album_artist,
            duration=metadata.duration,
            year=metadata.year,
            date=metadata.date,
            track_number=metadata.track_number,
            track_count=metadata.track_count,
            explicit=metadata.explicit,
            cover_url=metadata.cover_url,
            is_song=metadata.is_song,
            id=metadata.id,
            url=metadata.url,
            lyrics=None,
        )

        return data

    def to_yumee(self) -> YumeeSongMetadata:
        metadata = YumeeSongMetadata(
            title=self.name,
            artist=self.artist,
            artists=self.artists,
            album_name=self.album_name,
            album_artist=self.album_artist,
            track_number=self.track_number,
            track_count=self.track_count,
            disc_number=self.disc_number,
            disc_count=self.disc_count,
            genres=self.genres,
            date=self.date,
            year=self.year,
            lyrics=self.lyrics,
            cover_url=self.cover_url,
            explicit=self.explicit,
            origin_website=self.url,
        )

        return metadata
