from taipan_di import ServiceCollection

from medl.main.classes import (
    Downloader,
    FfmpegConverter,
    Parallelizer,
    PathFormatter,
)
from medl.main.interfaces import (
    BaseFfmpegConverter,
    BaseDownloader,
    BaseParallelizer,
    BasePathFormatter,
)

__all__ = ["add_tools"]


def add_tools(services: ServiceCollection) -> ServiceCollection:
    services.register(BaseDownloader).as_factory().with_implementation(Downloader)
    services.register(BaseFfmpegConverter).as_factory().with_implementation(FfmpegConverter)
    services.register(BaseParallelizer).as_factory().with_implementation(Parallelizer)
    services.register(BasePathFormatter).as_factory().with_implementation(PathFormatter)

    return services
