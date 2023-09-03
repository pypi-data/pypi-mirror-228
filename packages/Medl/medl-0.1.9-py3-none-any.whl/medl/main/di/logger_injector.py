from taipan_di import ServiceCollection

from medl.main.classes import (
    DownloadUrlFinderLogger,
    LyricsFetcherLogger,
    MetadataEmbedderLogger,
    TrackConverterLogger,
    TrackDownloaderLogger,
    MetadataFetcherLogger,
)
from medl.main.interfaces import (
    BaseDownloadUrlFinderLogger,
    BaseLyricsFetcherLogger,
    BaseMetadataEmbedderLogger,
    BaseTrackConverterLogger,
    BaseTrackDownloaderLogger,
    BaseMetadataFetcherLogger,
)

__all__ = ["add_loggers"]


def add_loggers(services: ServiceCollection) -> ServiceCollection:
    services.register(BaseDownloadUrlFinderLogger).as_factory().with_implementation(
        DownloadUrlFinderLogger
    )
    services.register(BaseLyricsFetcherLogger).as_factory().with_implementation(
        LyricsFetcherLogger
    )
    services.register(BaseMetadataEmbedderLogger).as_factory().with_implementation(
        MetadataEmbedderLogger
    )
    services.register(BaseTrackConverterLogger).as_factory().with_implementation(
        TrackConverterLogger
    )
    services.register(BaseTrackDownloaderLogger).as_factory().with_implementation(
        TrackDownloaderLogger
    )
    services.register(BaseMetadataFetcherLogger).as_factory().with_implementation(
        MetadataFetcherLogger
    )

    return services
