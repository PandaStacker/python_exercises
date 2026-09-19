"""008 — Context managers and rollback

A context manager brackets a block with reliable setup and cleanup.  A class
implements `__enter__` and `__exit__`; a generator decorated with
`contextlib.contextmanager` places setup before `yield` and cleanup in
`finally` or exception handling around it.

`__exit__` receives exception details.  Returning a truthy value suppresses
that exception; returning false leaves it for the caller.  Cleanup should
usually occur either way.  Implement both class-based and generator-based
managers below and preserve the original exception behavior.
"""
from __future__ import annotations

from collections.abc import Iterator, MutableMapping, MutableSequence
from contextlib import contextmanager
from types import TracebackType
from typing import Any, Generic, Protocol, TypeVar

T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")


class Closable(Protocol):
    def close(self) -> None: ...


class closing(Generic[T]):
    """Manage an already-created object whose `close()` must always be called.

    `__enter__` returns that exact object.  `__exit__` closes it and never
    suppresses an exception from the block.
    """

    def __init__(self, resource: T) -> None:
        raise NotImplementedError

    def __enter__(self) -> T:
        raise NotImplementedError

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool:
        raise NotImplementedError


@contextmanager
def temporary_value(
    mapping: MutableMapping[K, V], key: K, value: V
) -> Iterator[MutableMapping[K, V]]:
    """Temporarily assign `mapping[key] = value`, then exactly restore state.

    If the key was absent, remove it on exit.  If present, restore its old
    value.  Do so after both normal and exceptional exits.  Yield the mapping.
    """
    raise NotImplementedError
    yield mapping


@contextmanager
def rollback_on_error(sequence: MutableSequence[T]) -> Iterator[MutableSequence[T]]:
    """Restore a sequence's shallow contents only when the block raises.

    Preserve successful edits.  On error replace the full slice with the
    original contents, then re-raise the same exception.  Yield the sequence.
    """
    raise NotImplementedError
    yield sequence

