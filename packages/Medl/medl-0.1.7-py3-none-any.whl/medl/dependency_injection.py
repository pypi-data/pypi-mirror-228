from taipan_di import ServiceCollection

from medl.common import add_common
from medl.main import add_main

__all__ = ["add_medl"]


def add_medl(services: ServiceCollection) -> ServiceCollection:
    add_common(services)
    add_main(services)

    return services
