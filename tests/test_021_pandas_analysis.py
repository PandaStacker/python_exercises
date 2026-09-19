from __future__ import annotations

import unittest

import pandas as pd
from pandas.testing import assert_frame_equal, assert_series_equal

from tests.support import load_exercise


class PandasAnalysisTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_exercise("021_pandas_analysis.py")

    def raw_sales(self) -> pd.DataFrame:
        return pd.DataFrame(
            [
                {"order_id": 2, "customer": " Ada ", "region": " east", "quantity": "2", "unit_price": "3.50", "purchased_at": "2026-02-02"},
                {"order_id": 1, "customer": "Grace", "region": "west", "quantity": "1", "unit_price": "10", "purchased_at": "2026-01-01"},
                {"order_id": 3, "customer": "Ada", "region": "east", "quantity": "bad", "unit_price": "4", "purchased_at": "2026-01-05"},
                {"order_id": 4, "customer": "Lin", "region": "north", "quantity": "3", "unit_price": "2", "purchased_at": "2026-01-20"},
                {"order_id": 5, "customer": " ", "region": "east", "quantity": "1", "unit_price": "1", "purchased_at": "2026-01-10"},
            ]
        )

    def test_clean_sales_is_vectorized_typed_and_non_mutating(self) -> None:
        raw = self.raw_sales()
        original = raw.copy(deep=True)
        result = self.module.clean_sales(raw)
        assert_frame_equal(raw, original)
        self.assertEqual(result["order_id"].tolist(), [1, 4, 2])
        self.assertEqual(result["customer"].tolist(), ["Grace", "Lin", "Ada"])
        self.assertEqual(result["revenue"].tolist(), [10.0, 6.0, 7.0])
        self.assertEqual(str(result["quantity"].dtype), "int64")
        self.assertIsInstance(result.index, pd.RangeIndex)
        self.assertIsInstance(result["purchased_at"].dtype, pd.DatetimeTZDtype)

    def test_missing_columns_are_reported_sorted(self) -> None:
        with self.assertRaisesRegex(
            ValueError, r"^missing columns: \['customer', 'purchased_at'\]$"
        ):
            self.module.clean_sales(pd.DataFrame(columns=[c for c in self.module.SALES_COLUMNS if c not in {"customer", "purchased_at"}]))

    def test_join_tiers_validates_relationship_and_fills_unknown(self) -> None:
        sales = self.module.clean_sales(self.raw_sales())
        customers = pd.DataFrame([{"customer": "Ada", "tier": "gold"}, {"customer": "Grace", "tier": "silver"}])
        result = self.module.join_customer_tiers(sales, customers)
        self.assertEqual(result["customer"].tolist(), sales["customer"].tolist())
        self.assertEqual(result["tier"].tolist(), ["silver", "unassigned", "gold"])
        duplicates = pd.concat([customers, customers.iloc[[0]]], ignore_index=True)
        with self.assertRaises(pd.errors.MergeError):
            self.module.join_customer_tiers(sales, duplicates)

    def test_grouped_summary(self) -> None:
        sales = self.module.clean_sales(self.raw_sales())
        result = self.module.customer_summary(sales)
        expected = pd.DataFrame(
            {"customer": ["Grace", "Ada", "Lin"], "orders": [1, 1, 1], "units": [1, 2, 3], "revenue": [10.0, 7.0, 6.0]}
        )
        assert_frame_equal(result, expected, check_dtype=False)
        empty = self.module.customer_summary(sales.iloc[0:0])
        self.assertEqual(empty.columns.tolist(), ["customer", "orders", "units", "revenue"])

    def test_monthly_revenue(self) -> None:
        sales = self.module.clean_sales(self.raw_sales())
        result = self.module.monthly_revenue(sales)
        expected = pd.Series([16.0, 7.0], index=pd.Index(["2026-01", "2026-02"], name="month"), name="revenue")
        assert_series_equal(result, expected)


if __name__ == "__main__":
    unittest.main()
