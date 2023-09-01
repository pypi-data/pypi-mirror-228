from pathlib import Path
from typing import Callable
from medl.common.interfaces import BaseOptionsManager, BaseInitializer

__all__ = ["FolderInitializer"]


class FolderInitializer(BaseInitializer):
    def __init__(self, options_manager: BaseOptionsManager) -> None:
        super().__init__()
        self._options = options_manager.get_options()
        
    def _handle(self, request: None, next: Callable[[None], None]) -> None:
        Path(self._options.song_folder).resolve().mkdir(
            mode=755, parents=True, exist_ok=True
        )
        Path(self._options.temp_folder).resolve().mkdir(
            mode=755, parents=True, exist_ok=True
        )
        
        return next(request)
