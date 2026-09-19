"""002 — The loop toolbox

`for` visits values from any iterable; it is not limited to lists or numeric
indexes. Python supplies tools that keep common loop jobs direct:

    for number, item in enumerate(items, start=1):  # index and value
    for left, right in zip(xs, ys, strict=True):    # aligned iterables
    for key, value in mapping.items():              # mapping pairs
    for start in range(0, len(values), size):       # numeric positions

Loops compose: a nested loop visits values inside values. `continue` skips to
the next iteration, while `break` ends the nearest loop. A `for` loop's `else`
runs only when iteration finishes without `break`, which helps a search that
found nothing. Use `while` when repetition ends because state changes, such as
following pagination tokens until there is no next token.

Each function deliberately targets one construct. Tests inspect a few bodies
as well as results because the point is to practice the loop forms.
"""
from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping, Sequence
from typing import Any


def numbered_names(users: Iterable[Mapping[str, Any]], start: int = 1) -> list[str]:
    """Use `enumerate(..., start=start)` to return labels like `1. Ada`."""
    raise NotImplementedError


def attach_scores(users: Iterable[Mapping[str, Any]], scores: Iterable[int]) -> list[dict[str, Any]]:
    """Pair with `zip(..., strict=True)` and return copied users with scores."""
    raise NotImplementedError


def first_user_with_tag(users: Iterable[Mapping[str, Any]], tag: str) -> Mapping[str, Any] | None:
    """Find the first matching normalized tag using `break` and `for ... else`."""
    raise NotImplementedError


def chunk_users(users: Sequence[Mapping[str, Any]], size: int) -> list[list[Mapping[str, Any]]]:
    """Chunk with `range` and slicing; require size > 0 with a clear ValueError."""
    raise NotImplementedError


def collect_pages(fetch_page: Callable[[str | None], tuple[Iterable[Mapping[str, Any]], str | None]]) -> list[Mapping[str, Any]]:
    """Use `while` to fetch from token None through a page returning next None."""
    raise NotImplementedError


def active_names(records: Iterable[Mapping[str, Any]]) -> list[str]:
    """Use `continue` to skip only records whose active value is exactly False."""
    raise NotImplementedError


def count_nested_tags(users: Iterable[Mapping[str, Any]]) -> dict[str, int]:
    """Count tags with nested loops; rebuild via sorted(counts.items())."""
    raise NotImplementedError
