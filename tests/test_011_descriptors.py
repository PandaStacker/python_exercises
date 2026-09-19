from __future__ import annotations

from decimal import Decimal
import unittest

from tests.support import load_exercise


class DescriptorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_exercise("011_descriptors.py")

    def test_values_are_normalized_and_kept_per_instance(self) -> None:
        Product = self.module.Product
        first = Product("  Notebook ", "5.50", 1)
        second = Product("Pen", 2)
        self.assertEqual(first.name, "Notebook")
        self.assertEqual(first.price, Decimal("5.50"))
        self.assertEqual(first.final_price, Decimal("4.50"))
        self.assertEqual(second.name, "Pen")
        first.name = " Journal "
        self.assertEqual(first.name, "Journal")
        self.assertEqual(second.name, "Pen")

    def test_class_access_returns_descriptor(self) -> None:
        self.assertIsInstance(self.module.Product.name, self.module.NonBlank)
        self.assertIsInstance(self.module.Product.price, self.module.NonNegativeDecimal)

    def test_validation_messages_use_assigned_attribute_name(self) -> None:
        Product = self.module.Product
        with self.assertRaisesRegex(TypeError, "^name must be a string$"):
            Product(123, 1)
        with self.assertRaisesRegex(ValueError, "^name must not be blank$"):
            Product(" ", 1)
        for value in ("not-a-number", -1, "NaN", "Infinity"):
            with self.subTest(value=value), self.assertRaisesRegex(
                ValueError, "^price must be a non-negative number$"
            ):
                Product("valid", value)

    def test_final_price_has_a_zero_floor(self) -> None:
        product = self.module.Product("Pen", "2.00", "3.50")
        self.assertEqual(product.final_price, Decimal("0"))


if __name__ == "__main__":
    unittest.main()

