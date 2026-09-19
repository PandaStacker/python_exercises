from __future__ import annotations

from decimal import Decimal
import unittest

from tests.support import load_exercise


class ErrorBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_exercise("012_error_boundaries.py")

    def test_parse_line_success(self) -> None:
        item = self.module.parse_line(" ABC-1 , 4 , 2.50 ", 7)
        self.assertEqual(item, self.module.InventoryItem("ABC-1", 4, Decimal("2.50")))

    def test_conversion_errors_are_chained(self) -> None:
        with self.assertRaises(self.module.InventoryFormatError) as caught:
            self.module.parse_line("A,many,2", 3)
        error = caught.exception
        self.assertEqual(error.line_number, 3)
        self.assertEqual(error.line, "A,many,2")
        self.assertEqual(error.reason, "invalid quantity")
        self.assertIsInstance(error.__cause__, ValueError)
        self.assertEqual(str(error), "line 3: invalid quantity ('A,many,2')")

        with self.assertRaises(self.module.InventoryFormatError) as caught:
            self.module.parse_line("A,2,money", 4)
        self.assertIsNotNone(caught.exception.__cause__)

    def test_semantic_errors_have_expected_reasons(self) -> None:
        cases = [
            ("A,1", "expected 3 fields"),
            (" ,1,2", "blank SKU"),
            ("A,-1,2", "quantity must be non-negative"),
            ("A,1,-2", "price must be non-negative"),
            ("A,1,NaN", "invalid price"),
        ]
        for line, reason in cases:
            with self.subTest(line=line), self.assertRaises(self.module.InventoryFormatError) as caught:
                self.module.parse_line(line, 1)
            self.assertEqual(caught.exception.reason, reason)

    def test_collecting_parser_keeps_order_and_physical_lines(self) -> None:
        items, errors = self.module.parse_inventory(
            ["A,1,2.00", "  ", "broken", "B,3,4.00", "C,-1,5"]
        )
        self.assertEqual([item.sku for item in items], ["A", "B"])
        self.assertEqual([error.line_number for error in errors], [3, 5])

    def test_strict_loader_raises_an_exception_group(self) -> None:
        with self.assertRaises(ExceptionGroup) as caught:
            self.module.load_inventory(["bad", "A,no,2"])
        group = caught.exception
        self.assertEqual(group.message, "invalid inventory")
        self.assertEqual(len(group.exceptions), 2)
        self.assertTrue(all(isinstance(e, self.module.InventoryFormatError) for e in group.exceptions))
        self.assertEqual(
            self.module.load_inventory(["A,1,2"]),
            [self.module.InventoryItem("A", 1, Decimal("2"))],
        )


if __name__ == "__main__":
    unittest.main()

