from taipan_di import ServiceCollection

from medl.main.classes import (
    DownloadUrlFinder,
    LyricsFetcher,
    MetadataEmbedder,
    TrackConverter,
    TrackDownloader,
    MetadataFetcher,
    PreDownloadHandler,
    PostDownloadHandler,
)
from medl.main.interfaces import (
    BaseDownloadUrlFinder,
    BaseLyricsFetcher,
    BaseMetadataEmbedder,
    BaseTrackConverter,
    BaseTrackDownloader,
    BaseMetadataFetcher,
    BasePreDownloadHandler,
    BasePostDownloadHandler,
)

__all__ = ["add_handlers"]


def add_handlers(services: ServiceCollection) -> ServiceCollection:
    services.register(BaseDownloadUrlFinder).as_factory().with_implementation(
        DownloadUrlFinder
    )
    services.register(BaseLyricsFetcher).as_factory().with_implementation(LyricsFetcher)
    services.register(BaseMetadataEmbedder).as_factory().with_implementation(
        MetadataEmbedder
    )
    services.register(BaseTrackConverter).as_factory().with_implementation(TrackConverter)
    services.register(BaseTrackDownloader).as_factory().with_implementation(TrackDownloader)
    services.register(BaseMetadataFetcher).as_factory().with_implementation(MetadataFetcher)

    services.register(BasePreDownloadHandler).as_factory().with_implementation(
        PreDownloadHandler
    )
    services.register(BasePostDownloadHandler).as_factory().with_implementation(
        PostDownloadHandler
    )

    return services
