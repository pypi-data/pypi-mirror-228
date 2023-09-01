from __future__ import annotations
from dataclasses import dataclass, field
from typing import List

from mumee import MetadataClientEnum
from medl.common.consts import MEDL_PATH, TEMP_MUSIC_PATH

__all__ = ["MedlOptions"]


@dataclass
class MedlOptions:
    song_folder: str = f"{str(MEDL_PATH)}/{'{date}'}"
    temp_folder: str = f"{str(TEMP_MUSIC_PATH)}"
    file_format: str = "{title} - {artists}"
    extension: str = "mp3"
    lyrics_providers: List[str] = field(default_factory=lambda: ["genius"])
    metadata_providers: List[MetadataClientEnum] = field(
        default_factory=lambda: [MetadataClientEnum.ALL]
    )
    overwrite: str = "skip"
    generate_m3u: bool = False
    threads: int = 4

    def copy(self) -> MedlOptions:
        return MedlOptions(
            song_folder=self.song_folder,
            file_format=self.file_format,
            extension=self.extension,
            lyrics_providers=self.lyrics_providers,
            metadata_providers=self.metadata_providers,
            overwrite=self.overwrite,
            generate_m3u=self.generate_m3u,
            threads=self.threads,
        )
