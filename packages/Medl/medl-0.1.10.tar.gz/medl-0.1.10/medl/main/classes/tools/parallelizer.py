import asyncio
import sys
from typing import List, TypeVar, Callable
from medl.common import BaseOptionsManager

__all__ = ["Parallelizer"]

T = TypeVar("T")
U = TypeVar("U")


class Parallelizer:
    def __init__(self, options_manager: BaseOptionsManager) -> None:
        options = options_manager.get_options()

        self._loop: asyncio.AbstractEventLoop = (
            asyncio.new_event_loop()
            if sys.platform != "win32"
            else asyncio.ProactorEventLoop()
        )
        asyncio.set_event_loop(self._loop)

        self._semaphore: asyncio.Semaphore = asyncio.Semaphore(options.threads)

    def run_in_parallel(self, method: Callable[[T], U], arguments: List[T]) -> List[U]:
        async def method_with_semaphore(arg: T):
            async with self._semaphore:
                return await self._loop.run_in_executor(None, method, arg)

        tasks = [method_with_semaphore(arg) for arg in arguments]
        results = list(self._loop.run_until_complete(asyncio.gather(*tasks)))

        return results
