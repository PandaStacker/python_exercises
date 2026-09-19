from __future__ import annotations

from dataclasses import FrozenInstanceError
from decimal import Decimal
import unittest

from tests.support import load_exercise


class DataclassModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_exercise("009_dataclass_models.py")

    def test_money_normalizes_and_has_exact_arithmetic(self) -> None:
        Money = self.module.Money
        price = Money(0.1, " cad ")
        self.assertEqual(price.amount, Decimal("0.1"))
        self.assertEqual(price.currency, "CAD")
        self.assertEqual(price + Money("0.20"), Money("0.30"))
        self.assertEqual(price * 3, Money("0.3"))
        self.assertEqual(3 * price, Money("0.3"))
        with self.assertRaises(FrozenInstanceError):
            price.amount = Decimal("2")

    def test_money_rejects_invalid_values(self) -> None:
        Money = self.module.Money
        for amount in ("NaN", "Infinity", "-Infinity"):
            with self.subTest(amount=amount), self.assertRaises(ValueError):
                Money(amount)
        for currency in ("CA", "C4D", "EURO"):
            with self.subTest(currency=currency), self.assertRaises(ValueError):
                Money("1", currency)
        with self.assertRaisesRegex(ValueError, "currency"):
            Money("1", "CAD") + Money("1", "USD")

    def test_line_items_validate_and_compute_total(self) -> None:
        Money, LineItem = self.module.Money, self.module.LineItem
        item = LineItem("  notebook ", 3, Money("2.50"))
        self.assertEqual(item.product, "notebook")
        self.assertEqual(item.total, Money("7.50"))
        for name, quantity in (("", 1), ("pen", 0), ("pen", 1.5), ("pen", True)):
            with self.subTest(name=name, quantity=quantity), self.assertRaises(ValueError):
                LineItem(name, quantity, Money("1"))

    def test_carts_do_not_share_lists_and_sum_items(self) -> None:
        Money, LineItem, Cart = self.module.Money, self.module.LineItem, self.module.Cart
        first, second = Cart(), Cart()
        first.add(LineItem("pen", 2, Money("1.25")))
        first.add(LineItem("book", 1, Money("4.00")))
        self.assertEqual(first.total(), Money("6.50"))
        self.assertEqual(second.items, [])
        self.assertEqual(second.total("usd"), Money("0", "USD"))


if __name__ == "__main__":
    unittest.main()

