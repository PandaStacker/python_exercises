from __future__ import annotations

import unittest

from tests.support import load_exercise


class LazyPipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_exercise("007_lazy_pipelines.py")

    def test_countdown_is_its_own_iterator(self) -> None:
        countdown = self.module.Countdown(3)
        self.assertIs(iter(countdown), countdown)
        self.assertEqual(list(countdown), [3, 2, 1, 0])
        with self.assertRaises(StopIteration):
            next(countdown)
        with self.assertRaises(ValueError):
            self.module.Countdown(-1)

    def test_take_does_not_overconsume(self) -> None:
        source = iter(range(10))
        self.assertEqual(self.module.take(3, source), [0, 1, 2])
        self.assertEqual(next(source), 3)
        self.assertEqual(self.module.take(0, source), [])
        self.assertEqual(next(source), 4)
        with self.assertRaisesRegex(ValueError, "count must be non-negative"):
            self.module.take(-1, source)

    def test_unique_is_lazy_and_supports_a_key(self) -> None:
        consumed = []

        def source():
            for word in ["Ada", "ADA", "Grace", "ada", "Lin"]:
                consumed.append(word)
                yield word

        unique = self.module.unique_everseen(source(), key=str.casefold)
        self.assertEqual(consumed, [])
        self.assertEqual(next(unique), "Ada")
        self.assertEqual(consumed, ["Ada"])
        self.assertEqual(list(unique), ["Grace", "Lin"])

    def test_windowed_is_lazy_and_handles_boundaries(self) -> None:
        source = iter(range(100))
        windows = self.module.windowed(source, 3)
        self.assertEqual(next(windows), (0, 1, 2))
        self.assertEqual(next(source), 3, "first window should consume exactly three values")
        self.assertEqual(list(self.module.windowed([1, 2], 3)), [])
        self.assertEqual(list(self.module.windowed([1, 2, 3], 1)), [(1,), (2,), (3,)])
        with self.assertRaises(ValueError):
            next(self.module.windowed([1], 0))


if __name__ == "__main__":
    unittest.main()

