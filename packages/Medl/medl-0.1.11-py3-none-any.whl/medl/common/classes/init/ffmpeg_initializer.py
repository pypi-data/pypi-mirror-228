import shutil
from typing import Callable
import static_ffmpeg

from medl.common.interfaces import BaseInitializer

__all__ = ["FfmpegInitializer"]


class FfmpegInitializer(BaseInitializer):
    def __init__(self) -> None:
        super().__init__()

    def _handle(self, request: None, next: Callable[[None], None]) -> None:
        if shutil.which("ffmpeg") is None:
            result = static_ffmpeg.add_paths()

        return next(request)
