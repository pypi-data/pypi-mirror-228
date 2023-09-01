from taipan_di import ServiceCollection

from medl.main.classes import MusicToolbox
from medl.main.interfaces import BaseMusicToolbox
from medl.main.di import add_tools, add_loggers, add_handlers

from lyrics_client import add_lyrics_client
from yumee import add_yumee
from mumee import add_mumee

__all__ = ["add_main"]


def add_main(services: ServiceCollection) -> ServiceCollection:
    add_mumee(services)
    add_yumee(services)
    add_lyrics_client(services)

    add_tools(services)
    add_loggers(services)
    add_handlers(services)

    services.register(BaseMusicToolbox).as_factory().with_implementation(MusicToolbox)

    return services
