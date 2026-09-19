"""005 — Closures and captured state

A nested function closes over names from the scope where it was created.  It
can keep private state between calls without a class.  Use `nonlocal` when the
nested function must rebind a captured name; mutating a captured dictionary
does not require `nonlocal` because the name still refers to the same object.

Closures are created at runtime.  Be alert to late binding: functions made in
a loop all see the same loop variable unless each iteration captures its
current value (commonly through a helper scope or a default argument).
"""
from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import TypeVar

T = TypeVar("T")
R = TypeVar("R")


def make_counter(start: int = 0, step: int = 1) -> Callable[[], int]:
    """Return a function that advances and returns a private counter.

    The first call returns `start + step`, the second `start + 2 * step`, etc.
    Separate counters must have independent state.
    """
    raise NotImplementedError


def make_running_average() -> Callable[[float], float]:
    """Return a function reporting the arithmetic mean of all values seen."""
    raise NotImplementedError


def make_multipliers(factors: Iterable[int]) -> list[Callable[[int], int]]:
    """Return one multiplier function per factor, in the same order.

    Each returned function must remember its own factor after the loop ends.
    """
    raise NotImplementedError


def memoize_unary(function: Callable[[T], R]) -> Callable[[T], R]:
    """Cache a one-argument function's results by argument.

    Repeated calls with an equal, hashable argument must return the cached
    result without calling `function` again.  Attach the actual cache mapping
    to the returned function as an attribute named `cache` so callers can
    inspect or clear it.
    """
    raise NotImplementedError

