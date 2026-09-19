from __future__ import annotations

import unittest

from tests.support import load_exercise


class FunctionValueTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_exercise("004_functions_as_values.py")

    def test_group_by_preserves_order(self) -> None:
        words = ["pear", "fig", "plum", "kiwi", "pea"]
        grouped = self.module.group_by(words, len)
        self.assertEqual(list(grouped), [4, 3])
        self.assertEqual(grouped, {4: ["pear", "plum", "kiwi"], 3: ["fig", "pea"]})

    def test_partition_consumes_a_generator_once(self) -> None:
        seen = []

        def source():
            for value in range(6):
                seen.append(value)
                yield value

        even, odd = self.module.partition(lambda value: value % 2 == 0, source())
        self.assertEqual(even, [0, 2, 4])
        self.assertEqual(odd, [1, 3, 5])
        self.assertEqual(seen, list(range(6)))

    def test_compose_direction_and_identity(self) -> None:
        clean_length = self.module.compose(len, str.strip)
        self.assertEqual(clean_length("  python  "), 6)
        marker = object()
        self.assertIs(self.module.compose()(marker), marker)

    def test_multi_key_sort_is_stable(self) -> None:
        rows = [
            {"team": "b", "score": 2, "id": 1},
            {"team": "a", "score": 3, "id": 2},
            {"team": "a", "score": 1, "id": 3},
            {"team": "a", "score": 1, "id": 4},
        ]
        result = self.module.sort_by_many(
            rows, lambda row: row["team"], lambda row: row["score"]
        )
        self.assertEqual([row["id"] for row in result], [3, 4, 2, 1])
        self.assertEqual([row["id"] for row in rows], [1, 2, 3, 4])
        with self.assertRaisesRegex(ValueError, "at least one key is required"):
            self.module.sort_by_many(rows)


if __name__ == "__main__":
    unittest.main()

