from dataclasses import dataclass

__all__ = ["DownloadInfo"]


@dataclass
class DownloadInfo:
    id: str
    ext: str
    bitrate: str
    download_path: str
