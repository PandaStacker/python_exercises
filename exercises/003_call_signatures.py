"""003 — Call signatures and unpacking

A function signature is part of its interface.  `/` makes parameters before
it positional-only; `*` makes later parameters keyword-only.  `*args` gathers
extra positional arguments and `**kwargs` gathers extra keyword arguments.

Defaults also have semantics.  `None` is often meaningful, so a unique sentinel
object is the reliable way to distinguish “the caller omitted this argument”
from “the caller explicitly passed None.”

Complete the functions without weakening the supplied signatures.  The tests
exercise both their results and the ways callers are allowed to invoke them.
"""
from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any

MISSING = object()


def format_address(
    name: str,
    /,
    *,
    city: str,
    region: str | None = None,
    country: str = "Canada",
) -> str:
    """Format `name — city[, region], country`.

    Omit the region and its comma when region is `None` or an empty string.
    `name` is positional-only; all address fields are keyword-only.
    """
    raise NotImplementedError


def merge_settings(
    base: Mapping[str, Any],
    /,
    *overrides: Mapping[str, Any],
    **changes: Any,
) -> dict[str, Any]:
    """Return merged settings without modifying any input mapping.

    Start with `base`, apply every positional override from left to right, and
    finally apply keyword changes.  Later values win.
    """
    raise NotImplementedError


def update_profile(
    profile: Mapping[str, Any],
    /,
    *,
    name: Any = MISSING,
    email: Any = MISSING,
    bio: Any = MISSING,
) -> dict[str, Any]:
    """Return a copy with exactly the explicitly supplied fields updated.

    Passing `None` is an explicit update and must not be confused with omitting
    a field.  Preserve unrelated keys from the original mapping.
    """
    raise NotImplementedError


def invoke(
    function: Callable[..., Any],
    /,
    *args: Any,
    transform: Callable[[Any], Any] | None = None,
    **kwargs: Any,
) -> Any:
    """Forward args/kwargs to `function`, then optionally transform its result.

    `transform` belongs to `invoke`; do not forward it to `function`.
    """
    raise NotImplementedError

