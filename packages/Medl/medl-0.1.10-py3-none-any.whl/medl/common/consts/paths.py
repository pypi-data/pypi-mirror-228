import os
from pathlib import Path

__all__ = ["MEDL_PATH", "TEMP_MUSIC_PATH"]


MEDL_PATH = Path(os.path.expanduser("~"), ".medl")
TEMP_MUSIC_PATH = MEDL_PATH / "temp"
