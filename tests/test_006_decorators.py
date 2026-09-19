from __future__ import annotations

import unittest

from tests.support import load_exercise


class DecoratorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_exercise("006_decorators.py")

    def test_count_calls_counts_failures_and_preserves_metadata(self) -> None:
        @self.module.count_calls
        def reciprocal(value: float) -> float:
            """Return one divided by value."""
            return 1 / value

        self.assertEqual(reciprocal.calls, 0)
        self.assertEqual(reciprocal(2), 0.5)
        with self.assertRaises(ZeroDivisionError):
            reciprocal(0)
        self.assertEqual(reciprocal.calls, 2)
        self.assertEqual(reciprocal.__name__, "reciprocal")
        self.assertEqual(reciprocal.__doc__, "Return one divided by value.")

    def test_require_rejects_before_calling(self) -> None:
        calls = []

        @self.module.require(lambda value: value > 0, "must be positive")
        def double(value, *, rounded=False):
            calls.append(value)
            result = value * 2
            return round(result) if rounded else result

        self.assertEqual(double(2.5, rounded=True), 5)
        with self.assertRaisesRegex(ValueError, "^must be positive$"):
            double(-1)
        self.assertEqual(calls, [2.5])
        with self.assertRaises(TypeError):
            double()

    def test_retry_stops_at_success(self) -> None:
        attempts = []

        @self.module.retry(4, (LookupError,))
        def eventually(value):
            attempts.append(value)
            if len(attempts) < 3:
                raise KeyError("not yet")
            return value.upper()

        self.assertEqual(eventually("ok"), "OK")
        self.assertEqual(attempts, ["ok", "ok", "ok"])
        self.assertEqual(eventually.__name__, "eventually")

    def test_retry_reraises_final_instance_and_ignores_other_errors(self) -> None:
        errors = [ValueError("first"), ValueError("last")]

        @self.module.retry(2, (ValueError,))
        def fail():
            raise errors.pop(0)

        with self.assertRaises(ValueError) as caught:
            fail()
        self.assertEqual(str(caught.exception), "last")

        @self.module.retry(5, (ValueError,))
        def wrong_error():
            raise TypeError("do not retry")

        with self.assertRaisesRegex(TypeError, "do not retry"):
            wrong_error()
        with self.assertRaises(ValueError):
            self.module.retry(0)


if __name__ == "__main__":
    unittest.main()
