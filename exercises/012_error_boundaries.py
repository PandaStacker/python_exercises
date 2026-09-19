"""012 — Errors at system boundaries

External text can fail in several independent ways.  Parse it at one boundary,
translate low-level exceptions into errors meaningful to your application, and
decide whether callers want fail-fast or collect-all behavior.

`raise NewError(...) from original` preserves the causal traceback.  An
`ExceptionGroup` (Python 3.11+) reports several independent errors together.
This exercise uses both while keeping successfully parsed records available in
the non-strict API.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Iterable


@dataclass(frozen=True, slots=True)
class InventoryItem:
    sku: str
    quantity: int
    price: Decimal


class InventoryFormatError(ValueError):
    """A bad inventory line with public line_number, line, and reason fields."""

    def __init__(self, line_number: int, line: str, reason: str) -> None:
        """Use message `line <n>: <reason> (<line repr>)`."""
        raise NotImplementedError


def parse_line(line: str, line_number: int) -> InventoryItem:
    """Parse `SKU,QUANTITY,PRICE` into an InventoryItem.

    Strip every field.  Require exactly three fields and a non-blank SKU.
    Quantity must parse as an integer and be non-negative.  Price must parse as
    a Decimal, be finite, and be non-negative.

    Reasons are exactly: `expected 3 fields`, `blank SKU`, `invalid quantity`,
    `quantity must be non-negative`, `invalid price`, or
    `price must be non-negative`.  Chain integer/Decimal conversion errors as
    causes of the corresponding InventoryFormatError.
    """
    raise NotImplementedError


def parse_inventory(lines: Iterable[str]) -> tuple[list[InventoryItem], list[InventoryFormatError]]:
    """Parse all non-blank lines, collecting successes and errors in order.

    Physical line numbering starts at one.  Whitespace-only lines are ignored
    but still count toward the line number.
    """
    raise NotImplementedError


def load_inventory(lines: Iterable[str]) -> list[InventoryItem]:
    """Return parsed items or raise all format errors as an ExceptionGroup.

    The group message is `invalid inventory` and its contained exceptions are
    the InventoryFormatError objects returned by `parse_inventory`.
    """
    raise NotImplementedError

