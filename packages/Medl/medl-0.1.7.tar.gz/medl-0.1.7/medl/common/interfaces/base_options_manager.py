from typing import Protocol
from medl.common.data import MedlOptions

__all__ = ["BaseOptionsManager"]


class BaseOptionsManager(Protocol):
    def set_options(self, options: MedlOptions) -> None:
        ...

    def get_options(self) -> MedlOptions:
        ...
