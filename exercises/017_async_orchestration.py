"""017 — Async orchestration

Coroutines cooperate while waiting; tasks schedule coroutines to make progress
concurrently.  Real orchestration also needs limits and cleanup.  A semaphore
caps work in flight.  When one task makes the overall operation fail, cancel
and await its siblings so background work and warnings do not leak out.

These helpers are about control flow, not networking, so tests use tiny local
coroutines.  Preserve input order where promised even though completion order
differs.  `CancelledError` is a `BaseException` in modern Python: do not turn
cancellation into an ordinary retry or failure result.
"""
from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator, Awaitable, Callable, Iterable
from typing import Any, TypeVar

T = TypeVar("T")
R = TypeVar("R")
MISSING = object()


async def bounded_map(
    function: Callable[[T], Awaitable[R]],
    items: Iterable[T],
    *,
    limit: int,
) -> list[R]:
    """Run async `function` for every item with at most `limit` calls active.

    Require a positive limit.  Return results in input order.  On any worker
    exception, cancel and await unfinished sibling tasks, then re-raise the
    original exception.
    """
    raise NotImplementedError


async def first_success(awaitables: Iterable[Awaitable[T]]) -> T:
    """Return the first successfully completed result.

    Schedule every awaitable.  Ignore ordinary exceptions while other tasks
    can still succeed.  On success cancel and await unfinished tasks.  With no
    awaitables raise `ValueError("at least one awaitable is required")`.  If all
    fail, raise `ExceptionGroup("all operations failed", errors)` containing
    their exceptions.  If this coroutine is cancelled, clean up all children
    and allow cancellation to propagate.
    """
    # Avoid "coroutine was never awaited" noise while this starter is still
    # unfinished.  Replace this cleanup along with the exception.
    for awaitable in awaitables:
        close = getattr(awaitable, "close", None)
        if close is not None:
            close()
    raise NotImplementedError


async def with_timeout(
    awaitable: Awaitable[T],
    seconds: float,
    *,
    fallback: Any = MISSING,
) -> T:
    """Await an operation for at most `seconds`.

    On timeout, return an explicitly supplied fallback (including None).
    Without a fallback, re-raise `TimeoutError`.  The timed-out operation must
    be cancelled and awaited; `asyncio.wait_for` provides those semantics.
    """
    close = getattr(awaitable, "close", None)
    if close is not None:
        close()
    raise NotImplementedError


if __name__ == "__main__":
    print("--- Testing async orchestration ---")
    async def test():
        async def work(x): return x * 2
        try:
            res = await bounded_map(work, [1, 2, 3], limit=2)
            print("bounded_map:", res)
        except Exception as e:
            print(f"bounded_map Error: {e!r}")
    try:
        asyncio.run(test())
    except Exception as e:
        print(f"Error: {e!r}")
