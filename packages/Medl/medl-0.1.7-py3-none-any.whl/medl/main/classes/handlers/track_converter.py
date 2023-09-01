from pathlib import Path
from typing import Optional
from medl.common import SongData, MedlException
from medl.main.data import DownloadInfo
from medl.main.interfaces import (
    BaseTrackConverterLogger,
    BasePathFormatter,
    BaseFfmpegConverter,
)

__all__ = ["TrackConverter"]


class TrackConverter:
    def __init__(
        self,
        logger: BaseTrackConverterLogger,
        path_formatter: BasePathFormatter,
        ffmpeg_converter: BaseFfmpegConverter,
    ) -> None:
        self._logger = logger
        self._formatter = path_formatter
        self._ffmpeg_converter = ffmpeg_converter

    def convert(self, track_data: SongData, download_info: DownloadInfo) -> Optional[Path]:
        self._logger.start_converting(track_data)

        tmp_path = Path(download_info.download_path)
        new_path = self._formatter.format(track_data)

        try:
            self._ffmpeg_converter.convert(tmp_path, new_path)

            self._logger.converted(track_data)
            return new_path
        except MedlException as ex:
            self._logger.error_converting(track_data, str(ex))
            return None
        finally:
            if tmp_path.exists():
                tmp_path.unlink()
