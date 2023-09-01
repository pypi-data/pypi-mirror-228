from typing import List, TypeVar, Callable, Protocol

__all__ = ["BaseParallelizer"]

T = TypeVar("T")
U = TypeVar("U")


class BaseParallelizer(Protocol):
    def run_in_parallel(self, method: Callable[[T], U], arguments: List[T]) -> List[U]:
        ...
