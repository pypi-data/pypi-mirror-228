from yt_dlp import YoutubeDL
from medl.main.data import DownloadInfo
from medl.common import MedlException, BaseOptionsManager

__all__ = ["Downloader"]


class Downloader:
    def __init__(self, options_manager: BaseOptionsManager) -> None:
        self._options = options_manager.get_options()

        if self._options.extension == "m4a":
            ytdl_format = "bestaudio[ext=m4a]/bestaudio/best"
        elif self._options.extension == "opus":
            ytdl_format = "bestaudio[ext=webm]/bestaudio/best"
        else:
            ytdl_format = "bestaudio"

        yt_dlp_options = {
            "format": ytdl_format,
            "quiet": True,
            "no_warnings": True,
            "encoding": "UTF-8",
            # "cookiefile": self.cookie_file,
            "outtmpl": f"{self._options.temp_folder}/%(id)s.%(ext)s",
            "retries": 5,
        }

        self._youtube_dl = YoutubeDL(yt_dlp_options)

    def download(self, url: str) -> DownloadInfo:
        info = self._youtube_dl.extract_info(url, download=True)

        if info is None:
            raise MedlException("Couldn't download music from URL %s", url)

        return DownloadInfo(
            id=info["id"],
            ext=info["ext"],
            bitrate=info["abr"],
            download_path=f"{self._options.temp_folder}/{info['id']}.{info['ext']}",
        )
