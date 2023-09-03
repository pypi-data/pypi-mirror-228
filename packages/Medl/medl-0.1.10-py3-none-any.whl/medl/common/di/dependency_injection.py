from taipan_di import ServiceCollection

from medl.common.interfaces import BaseLogger, BaseOptionsManager, BaseInitializer
from medl.common.classes import (
    Logger,
    LogFormatter,
    OptionsManager,
    FfmpegInitializer,
    FolderInitializer,
)

__all__ = ["add_common"]


def add_common(services: ServiceCollection) -> ServiceCollection:
    services.register(BaseLogger).as_singleton().with_implementation(Logger)
    services.register(LogFormatter).as_singleton().with_self()

    services.register(BaseOptionsManager).as_singleton().with_implementation(OptionsManager)

    services.register_pipeline(BaseInitializer).add(FfmpegInitializer).add(
        FolderInitializer
    ).as_singleton()

    return services
