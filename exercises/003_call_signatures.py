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
    
    Elaboration: 
    - The `/` means `name` MUST be passed by position (e.g. `format_address("Alice", ...)`).
    - The `*` means everything after it MUST be passed by keyword (e.g. `city="Paris"`).
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
    
    Elaboration:
    - `*overrides` collects any extra positional arguments into a tuple.
    - `**changes` collects any extra keyword arguments into a dictionary.
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
    
    Elaboration:
    - `MISSING` is a custom object we created at the top of the file.
    - We use it instead of `None` as the default value so we can tell the difference
      between a user omitting the argument and a user explicitly passing `None`.
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
    
    Elaboration:
    This function acts as a wrapper. It takes a function, calls it with whatever
    arguments were provided, and then optionally runs a transformation on the output.
    """
    raise NotImplementedError


if __name__ == "__main__":
    print("--- Testing format_address ---")
    try:
        print(format_address("Alice", city="Wonderland", country="UK"))
    except Exception as e:
        print(f"Error: {e!r}")

    print("\n--- Testing merge_settings ---")
    try:
        base = {"theme": "light", "port": 8080}
        override = {"port": 9000}
        print(merge_settings(base, override, debug=True))
    except Exception as e:
        print(f"Error: {e!r}")

