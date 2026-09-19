"""007 — Lazy iterator pipelines

An iterable can create an iterator; an iterator remembers a current position
and produces values through `__next__`.  Generator functions implement that
protocol for you and, importantly, do no work until iteration asks for a value.

These utilities must work with one-shot generators and infinite inputs.  Do
not eagerly convert the input to a list.  Tests check not only the returned
values but how far upstream was consumed.
"""
from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator
from typing import Generic, TypeVar

T = TypeVar("T")
K = TypeVar("K")


class Countdown(Iterator[int]):
    """An iterator yielding `start` down through zero, then stopping.

    Require a non-negative integer start.  `iter(countdown)` must return the
    countdown object itself.  Once exhausted, it stays exhausted.
    """

    def __init__(self, start: int) -> None:
        raise NotImplementedError

    def __iter__(self) -> Countdown:
        raise NotImplementedError

    def __next__(self) -> int:
        raise NotImplementedError


def take(count: int, iterable: Iterable[T]) -> list[T]:
    """Collect at most `count` items, consuming no extra item.

    Raise `ValueError("count must be non-negative")` for a negative count.
    """
    raise NotImplementedError


def unique_everseen(
    iterable: Iterable[T], key: Callable[[T], K] | None = None
) -> Iterator[T]:
    """Yield the first item for each distinct key, preserving order.

    With no key function, use the item itself as its key.  Keys are hashable.
    This function must be lazy.
    """
    raise NotImplementedError
    yield  # Keep this a generator while it is unfinished.


def windowed(iterable: Iterable[T], size: int) -> Iterator[tuple[T, ...]]:
    """Yield each overlapping, full window of `size` items.

    `windowed([1, 2, 3, 4], 3)` yields `(1, 2, 3)`, then `(2, 3, 4)`.
    Yield nothing when the input is shorter than the window.  Require a
    positive size.  Consume only enough input to produce the next window.
    """
    raise NotImplementedError
    yield

