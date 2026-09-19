"""006 — Production-quality decorators

A decorator replaces one callable with another.  Useful decorators forward
arbitrary arguments, return the wrapped result, and preserve metadata with
`functools.wraps`.  A decorator factory adds another layer: configuration is
captured first, then the produced decorator receives the function.

Implement the three decorators below.  Notice where state belongs: retry state
is local to one call, while a call counter survives between calls.  Do not
catch `BaseException`; callers generally expect interrupts and system exits to
escape normal error handling.
"""
from __future__ import annotations

from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar

F = TypeVar("F", bound=Callable[..., Any])


def count_calls(function: F) -> F:
    """Return a metadata-preserving wrapper with a public `calls` count.

    Increment `wrapper.calls` before every attempted call, including calls
    where the wrapped function raises.  Each decorated function gets its own
    count starting at zero.
    """
    raise NotImplementedError


def require(
    predicate: Callable[[Any], bool], message: str
) -> Callable[[F], F]:
    """Create a decorator validating the first positional argument.

    If there is no positional argument, let normal Python call handling occur.
    When there is one and `predicate(value)` is false, raise `ValueError` with
    the supplied message without calling the wrapped function.
    """
    raise NotImplementedError


def retry(
    attempts: int,
    exceptions: tuple[type[Exception], ...] = (Exception,),
) -> Callable[[F], F]:
    """Create a decorator that makes at most `attempts` total attempts.

    Require `attempts >= 1`, raising `ValueError` while creating the decorator
    otherwise.  Retry only the supplied exception types.  After the last
    failure, re-raise that same exception instance.  Return immediately after
    a successful call and preserve the wrapped function's metadata.
    """
    raise NotImplementedError

