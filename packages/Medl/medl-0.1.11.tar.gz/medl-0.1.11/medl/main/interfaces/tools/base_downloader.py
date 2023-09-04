from typing import Protocol
from medl.main.data import DownloadInfo

__all__ = ["BaseDownloader"]


class BaseDownloader(Protocol):
    def download(self, url: str) -> DownloadInfo:
        ...
