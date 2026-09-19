"""014 — Protocols and generics as design tools

Typing is most useful when it clarifies relationships.  A generic repository
stores one consistent item type.  A Protocol describes the behavior a consumer
needs without requiring inheritance.  This is structural typing: any object
with the right operations can participate.

The annotations are part of this exercise, but the runtime behavior matters
too.  Keep `Reader` read-only so implementations can safely provide more
specific item types.  Return copies/views as documented so repository internals
cannot be mutated accidentally.
"""
from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator
from typing import Generic, Protocol, TypeVar, runtime_checkable

T = TypeVar("T")
T_co = TypeVar("T_co", covariant=True)


@runtime_checkable
class Identified(Protocol):
    id: str


class Reader(Protocol[T_co]):
    def get(self, item_id: str) -> T_co | None: ...

    def __iter__(self) -> Iterator[T_co]: ...


class InMemoryRepository(Generic[T]):
    """Insertion-ordered storage for items satisfying Identified at runtime.

    `add` rejects objects not conforming to Identified with `TypeError`, and
    duplicate ids with `ValueError("duplicate id: <id>")`.  `get` returns the
    stored object or None.  Iteration yields stored objects in insertion order.
    `remove` deletes and returns an item, raising KeyError for an absent id.
    """

    def __init__(self, items: Iterable[T] = ()) -> None:
        raise NotImplementedError

    def add(self, item: T) -> None:
        raise NotImplementedError

    def get(self, item_id: str) -> T | None:
        raise NotImplementedError

    def remove(self, item_id: str) -> T:
        raise NotImplementedError

    def __iter__(self) -> Iterator[T]:
        raise NotImplementedError


def find_first(reader: Reader[T_co], predicate: Callable[[T_co], bool]) -> T_co | None:
    """Return the first matching item from any Reader, or None."""
    raise NotImplementedError


def copy_matching(
    source: Reader[T],
    destination: InMemoryRepository[T],
    predicate: Callable[[T], bool],
) -> int:
    """Add matching source items to destination and return how many were added.

    Let the repository's normal duplicate-id error propagate.
    """
    raise NotImplementedError

