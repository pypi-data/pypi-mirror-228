from datetime import date, datetime
from pathlib import Path
from medl.common import SongData, BaseOptionsManager

__all__ = ["PathFormatter"]


class PathFormatter:
    def __init__(self, options_manager: BaseOptionsManager) -> None:
        self._options = options_manager.get_options()

    def format(self, track_data: SongData) -> Path:
        format = f"{self._options.song_folder}/{self._options.file_format}.{self._options.extension}"

        path_str = format
        path_str = path_str.replace("{title}", track_data.name)
        path_str = path_str.replace("{artists}", ", ".join(track_data.artists))
        path_str = path_str.replace(
            "{date}", f"{date.today().day}-{date.today().month}-{date.today().year}"
        )
        path_str = path_str.replace(
            "{time}",
            f"{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}",
        )

        return Path(path_str)
