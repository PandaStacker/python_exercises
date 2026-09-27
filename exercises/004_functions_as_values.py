"""004 — Functions as values

Python functions can be stored, passed, and returned like any other object.
Small callables let general algorithms delegate one decision: a key function
chooses what to sort or group by, while a predicate answers yes or no.

The important habit is to call the supplied function at the right time—not to
special-case the sample data.  Implement these general-purpose helpers using
iteration and function calls.  Preserve input order where the contract asks.
"""
from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import TypeVar

T = TypeVar("T")
K = TypeVar("K")
R = TypeVar("R")


def group_by(items: Iterable[T], key: Callable[[T], K]) -> dict[K, list[T]]:
    """Group items by `key(item)`, preserving item and first-seen key order."""
    raise NotImplementedError


def partition(predicate: Callable[[T], bool], items: Iterable[T]) -> tuple[list[T], list[T]]:
    """Return `(matching, non_matching)` lists while consuming `items` once."""
    raise NotImplementedError


def compose(*functions: Callable[[object], object]) -> Callable[[object], object]:
    """Return a function that applies the supplied functions right-to-left.

    `compose(f, g)(value)` means `f(g(value))`.  With no functions, return an
    identity function that returns its argument unchanged.
    """
    raise NotImplementedError


def sort_by_many(
    items: Iterable[T],
    *keys: Callable[[T], object],
    reverse: bool = False,
) -> list[T]:
    """Return a list sorted lexicographically by all key functions.

    `sort_by_many(rows, key1, key2)` compares `(key1(row), key2(row))`.
    Require at least one key and raise `ValueError("at least one key is required")`
    otherwise.  Rely on Python's stable sort for ties.
    """
    raise NotImplementedError


if __name__ == "__main__":
    sample_data = [{"id": 1, "val": 10}, {"id": 2, "val": 5}, {"id": 3, "val": 10}]

    print("--- Testing group_by ---")
    try:
        print(group_by(sample_data, key=lambda x: x["val"]))
    except Exception as e:
        print(f"Error: {e!r}")

    print("\n--- Testing partition ---")
    try:
        print(partition(lambda x: x["val"] > 5, sample_data))
    except Exception as e:
        print(f"Error: {e!r}")

