from medl.common.data import MedlOptions

__all__ = ["OptionsManager"]


class OptionsManager:
    def __init__(self) -> None:
        self._options: MedlOptions = MedlOptions()

    def set_options(self, options: MedlOptions) -> None:
        self._options = options

    def get_options(self) -> MedlOptions:
        return self._options
