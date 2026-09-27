"""011 — Managed attributes and descriptors

A property manages one named attribute on one class.  A descriptor packages
the same access policy for reuse: an object with `__get__` and `__set__` placed
on a class controls that attribute on every instance.  `__set_name__` tells the
descriptor which public name it was assigned to.

Store each instance's value under a private name such as `_name`.  When
`__get__` receives `instance is None`, return the descriptor itself so class-
level introspection works.  Keep state on each Product instance, never on the
shared descriptor.
"""
from __future__ import annotations

from decimal import Decimal, InvalidOperation
from typing import Any


class NonBlank:
    """Descriptor accepting strings after stripping surrounding whitespace.

    Reject a non-string with `TypeError("<name> must be a string")` and a blank
    value with `ValueError("<name> must not be blank")`.
    """

    def __set_name__(self, owner: type, name: str) -> None:
        # This setup is supplied so the unfinished module can still import.
        # The interesting work is using these names in __get__ and __set__.
        self.public_name = name
        self.private_name = f"_{name}"

    def __get__(self, instance: object | None, owner: type | None = None) -> Any:
        raise NotImplementedError

    def __set__(self, instance: object, value: str) -> None:
        raise NotImplementedError


class NonNegativeDecimal:
    """Descriptor storing a finite, non-negative Decimal.

    Convert with `Decimal(str(value))`.  Conversion failures, non-finite values,
    and negative values all raise `ValueError("<name> must be a non-negative number")`.
    """

    def __set_name__(self, owner: type, name: str) -> None:
        self.public_name = name
        self.private_name = f"_{name}"

    def __get__(self, instance: object | None, owner: type | None = None) -> Any:
        raise NotImplementedError

    def __set__(self, instance: object, value: object) -> None:
        raise NotImplementedError


class Product:
    """A product with descriptor-managed `name`, `price`, and `discount`."""

    name = NonBlank()
    price = NonNegativeDecimal()
    discount = NonNegativeDecimal()

    def __init__(self, name: str, price: object, discount: object = 0) -> None:
        raise NotImplementedError

    @property
    def final_price(self) -> Decimal:
        """Return `price - discount`, never falling below zero."""
        raise NotImplementedError


if __name__ == "__main__":
    print("--- Testing descriptors ---")
    try:
        p = Product("Widget", 10.50)
        print("Product name:", p.name)
        print("Final price:", p.final_price)
    except Exception as e:
        print(f"Error: {e!r}")
