"""009 — Dataclass domain models

Dataclasses generate repetitive methods, but modeling decisions remain yours.
Frozen value objects are useful for facts that should not change.  Mutable
aggregate objects can own collections and behavior.  Use `default_factory`
for a fresh list per instance, and validate invariants at construction so
invalid objects cannot drift through the program.

This exercise models money and a shopping cart.  Keep arithmetic exact with
`Decimal`; never route a float through `Decimal(float)`, which preserves its
binary approximation.  `Decimal(str(value))` is appropriate at this boundary.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any


@dataclass(frozen=True, order=True, slots=True)
class Money:
    """An immutable monetary amount in one currency.

    Fields are `amount: Decimal` and `currency: str = "CAD"`.
    In `__post_init__`, normalize amount with `Decimal(str(amount))` and
    currency by stripping and uppercasing it.  Because this class is frozen,
    assign normalized fields with `object.__setattr__`.

    Reject non-finite amounts and currencies that are not exactly three ASCII
    letters with `ValueError`.  Addition requires another Money in the same
    currency; return `NotImplemented` for another type and raise `ValueError`
    for mixed currencies.  Multiplication by an integer returns new Money and
    must work in either order (`money * 3` and `3 * money`).
    """

    amount: Decimal
    currency: str = "CAD"

    def __post_init__(self) -> None:
        raise NotImplementedError

    def __add__(self, other: object) -> Money:
        raise NotImplementedError

    def __mul__(self, quantity: int) -> Money:
        raise NotImplementedError

    __rmul__ = __mul__


@dataclass(frozen=True, slots=True)
class LineItem:
    """A product name, positive integer quantity, and unit price."""

    product: str
    quantity: int
    unit_price: Money

    def __post_init__(self) -> None:
        """Strip product and reject blank names or non-positive integer quantities."""
        raise NotImplementedError

    @property
    def total(self) -> Money:
        """Return quantity multiplied by unit price."""
        raise NotImplementedError


@dataclass
class Cart:
    """A mutable cart whose item list is never shared with another cart."""

    items: list[LineItem] = field(default_factory=list)

    def add(self, item: LineItem) -> None:
        """Append an item."""
        raise NotImplementedError

    def total(self, currency: str = "CAD") -> Money:
        """Sum item totals, starting at zero in the requested currency.

        Mixed currencies fail through Money's normal addition rule.
        """
        raise NotImplementedError

