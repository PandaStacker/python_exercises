from __future__ import annotations

import unittest

from tests.support import load_exercise


class ClosureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_exercise("005_closures.py")

    def test_counters_keep_independent_state(self) -> None:
        by_two = self.module.make_counter(10, 2)
        backwards = self.module.make_counter(0, -1)
        self.assertEqual([by_two(), by_two(), backwards(), by_two()], [12, 14, -1, 16])

    def test_running_average(self) -> None:
        average = self.module.make_running_average()
        self.assertEqual(average(10), 10)
        self.assertEqual(average(20), 15)
        self.assertAlmostEqual(average(-3), 9)

    def test_multipliers_do_not_late_bind_loop_variable(self) -> None:
        functions = self.module.make_multipliers([2, 3, 10])
        self.assertEqual([function(5) for function in functions], [10, 15, 50])

    def test_memoizer_caches_even_a_none_result(self) -> None:
        calls = []

        def lookup(value):
            calls.append(value)
            return None if value == "missing" else value.upper()

        cached = self.module.memoize_unary(lookup)
        self.assertEqual(cached("python"), "PYTHON")
        self.assertEqual(cached("python"), "PYTHON")
        self.assertIsNone(cached("missing"))
        self.assertIsNone(cached("missing"))
        self.assertEqual(calls, ["python", "missing"])
        self.assertEqual(cached.cache, {"python": "PYTHON", "missing": None})
        cached.cache.clear()
        cached("python")
        self.assertEqual(calls, ["python", "missing", "python"])


if __name__ == "__main__":
    unittest.main()

