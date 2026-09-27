"""027 — Protocols, adapters, and layered stores

Python abstractions do not need a deep inheritance tree. A small Protocol can
describe the behavior a layer needs; any object with that behavior works.
Adapters can then wrap one implementation to add namespacing, serialization,
caching, or temporary behavior. Composition keeps each concern independent.

Build these layers around mapping-like missing-key semantics: `get` and
`delete` raise KeyError for an absent key. The final test composes four classes,
demonstrating that every layer depends on an interface rather than a concrete
implementation.
"""
from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
import json
from typing import Any, Generic, Protocol, TypeVar, runtime_checkable

T = TypeVar("T")


@runtime_checkable
class Store(Protocol[T]):
    def get(self, key: str) -> T: ...
    def set(self, key: str, value: T) -> None: ...
    def delete(self, key: str) -> None: ...


class MemoryStore(Generic[T]):
    """A Store backed by a private dictionary."""

    def __init__(self) -> None:
        raise NotImplementedError

    def get(self, key: str) -> T:
        raise NotImplementedError

    def set(self, key: str, value: T) -> None:
        raise NotImplementedError

    def delete(self, key: str) -> None:
        raise NotImplementedError


class NamespacedStore(Generic[T]):
    """Adapt a Store by prefixing every underlying key with `<namespace>:`."""

    def __init__(self, inner: Store[T], namespace: str) -> None:
        """Strip namespace and reject blank with ValueError."""
        raise NotImplementedError

    def get(self, key: str) -> T:
        raise NotImplementedError

    def set(self, key: str, value: T) -> None:
        raise NotImplementedError

    def delete(self, key: str) -> None:
        raise NotImplementedError


class JsonStore:
    """Adapt a string Store to transparently hold JSON-compatible values."""

    def __init__(self, inner: Store[str]) -> None:
        raise NotImplementedError

    def get(self, key: str) -> Any:
        """Decode the inner string with json.loads."""
        raise NotImplementedError

    def set(self, key: str, value: Any) -> None:
        """Encode with json.dumps(value, sort_keys=True), then delegate."""
        raise NotImplementedError

    def delete(self, key: str) -> None:
        raise NotImplementedError


MISSING = object()


class CachedStore(Generic[T]):
    """Cache both values and missing-key results from another Store.

    The public `cache` dictionary maps keys to values or the MISSING sentinel.
    A cached MISSING must raise KeyError without consulting inner again. `set`
    and `delete` update inner first, then keep the cache coherent.
    """

    def __init__(self, inner: Store[T]) -> None:
        raise NotImplementedError

    def get(self, key: str) -> T:
        raise NotImplementedError

    def set(self, key: str, value: T) -> None:
        raise NotImplementedError

    def delete(self, key: str) -> None:
        raise NotImplementedError


@contextmanager
def temporary_value(store: Store[T], key: str, value: T) -> Iterator[Store[T]]:
    """Set a value for the block, then restore the old value or absence.

    Restore after normal or exceptional exit, yield the same store, and never
    suppress the block's exception. Use MISSING to distinguish absent from a
    stored value such as None.
    """
    raise NotImplementedError
    yield store


if __name__ == "__main__":
    print("--- Testing layered stores ---")
    try:
        store = MemoryStore()
        ns_store = NamespacedStore(store, "test")
        ns_store.set("key", "value")
        print("ns_store.get('key'):", ns_store.get("key"))
    except Exception as e:
        print(f"Error: {e!r}")
