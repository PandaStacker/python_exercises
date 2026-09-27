"""026 — Designing a fluent, lazy abstraction

Python makes small abstractions pleasant because functions are values, objects
can implement language protocols, and closures retain configuration. Here you
will combine those strengths into a reusable Pipeline—not merely implement a
collection of unrelated helpers.

A Pipeline stores a zero-argument *iterator factory*, not an iterator. That one
choice makes pipelines lazy and allows a fresh traversal each time. Each fluent
operator returns a new Pipeline whose factory closes over its upstream pipeline
and operation. `__iter__` integrates it with every Python consumer, while
`__or__` permits reusable stages to compose with `|`.

Do not materialize intermediate lists. Work must begin only when iteration or
`reduce` requests values.
"""
from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator
from typing import Generic, TypeVar

T = TypeVar("T")
U = TypeVar("U")
A = TypeVar("A")


class Pipeline(Generic[T]):
    """A reusable, lazy sequence of transformations."""

    def __init__(self, factory: Callable[[], Iterator[T]]) -> None:
        """Store the iterator factory without calling it."""
        raise NotImplementedError

    @classmethod
    def from_factory(cls, factory: Callable[[], Iterator[T]]) -> Pipeline[T]:
        """Construct a pipeline around a repeatable iterator factory."""
        raise NotImplementedError

    @classmethod
    def of(cls, *values: T) -> Pipeline[T]:
        """Construct a reusable pipeline over the supplied values."""
        raise NotImplementedError

    def __iter__(self) -> Iterator[T]:
        """Return a fresh iterator produced by the stored factory."""
        raise NotImplementedError

    def map(self, function: Callable[[T], U]) -> Pipeline[U]:
        """Return a lazy pipeline applying function to each value."""
        raise NotImplementedError

    def where(self, predicate: Callable[[T], bool]) -> Pipeline[T]:
        """Return a lazy pipeline retaining values satisfying predicate."""
        raise NotImplementedError

    def flat_map(self, function: Callable[[T], Iterable[U]]) -> Pipeline[U]:
        """Map each value to an iterable and lazily flatten one level."""
        raise NotImplementedError

    def tap(self, effect: Callable[[T], object]) -> Pipeline[T]:
        """Run a side effect lazily for each value, then yield that same value."""
        raise NotImplementedError

    def take(self, count: int) -> Pipeline[T]:
        """Return at most count values without over-consuming upstream.

        Raise `ValueError("count must be non-negative")` for a negative count.
        `itertools.islice` is useful here.
        """
        raise NotImplementedError

    def reduce(self, initial: A, combine: Callable[[A, T], A]) -> A:
        """Eagerly fold values left-to-right, beginning with initial."""
        raise NotImplementedError

    def __or__(self, stage: Callable[[Pipeline[T]], Pipeline[U]]) -> Pipeline[U]:
        """Apply a reusable pipeline stage, enabling `pipeline | stage`."""
        raise NotImplementedError


def mapping(function: Callable[[T], U]) -> Callable[[Pipeline[T]], Pipeline[U]]:
    """Return a stage that calls Pipeline.map with function."""
    raise NotImplementedError


def filtering(predicate: Callable[[T], bool]) -> Callable[[Pipeline[T]], Pipeline[T]]:
    """Return a stage that calls Pipeline.where with predicate."""
    raise NotImplementedError


if __name__ == "__main__":
    print("--- Testing fluent pipeline ---")
    try:
        p = Pipeline.of(1, 2, 3, 4)
        result = p.map(lambda x: x * 2).where(lambda x: x > 4).reduce(0, lambda a, b: a + b)
        print("Pipeline result:", result)
    except Exception as e:
        print(f"Error: {e!r}")
