from __future__ import annotations

import ast
import inspect
import textwrap
import unittest

import numpy as np
from numpy.testing import assert_allclose, assert_array_equal

from tests.support import load_exercise


class NumPyArrayTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_exercise("020_numpy_arrays.py")

    def test_standardize_columns_and_constant_column(self) -> None:
        values = np.array([[1, 10, 5], [2, 20, 5], [3, 30, 5]], dtype=np.int64)
        original = values.copy()
        result = self.module.standardize_columns(values)
        assert_allclose(result.mean(axis=0), [0, 0, 0], atol=1e-12)
        assert_allclose(result[:, :2].std(axis=0), [1, 1])
        assert_array_equal(result[:, 2], [0, 0, 0])
        self.assertEqual(result.dtype, np.float64)
        assert_array_equal(values, original)

    def test_pairwise_distances_uses_all_pairs(self) -> None:
        result = self.module.pairwise_distances([[0, 0], [3, 4], [3, 0]])
        assert_allclose(result, [[0, 5, 3], [5, 0, 4], [3, 4, 0]])

    def test_one_hot_uses_advanced_indexing(self) -> None:
        result = self.module.one_hot(np.array([2, 0, 1, 2]), 3)
        assert_array_equal(result, [[0, 0, 1], [1, 0, 0], [0, 1, 0], [0, 0, 1]])
        self.assertEqual(result.dtype, np.int64)
        for labels, classes in (([0], 0), ([3], 3), ([-1], 3), ([1.5], 3), ([[1]], 3)):
            with self.subTest(labels=labels, classes=classes), self.assertRaises(ValueError):
                self.module.one_hot(labels, classes)

    def test_channel_gains_broadcast_and_clip(self) -> None:
        image = np.array([[[10, 20, 30], [100, 200, 250]]], dtype=np.uint8)
        result = self.module.scale_channels(image, [2, 0.5, 1.5])
        assert_allclose(result, [[[20, 10, 45], [200, 100, 255]]])
        assert_array_equal(image, [[[10, 20, 30], [100, 200, 250]]])
        with self.assertRaisesRegex(ValueError, "incompatible image and gains"):
            self.module.scale_channels(image, [1, 2])

    def test_shape_errors_are_clear(self) -> None:
        for value in ([], [1, 2], [[[1]]]):
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, "expected a non-empty 2-D array"):
                self.module.standardize_columns(value)
        with self.assertRaises(ValueError):
            self.module.pairwise_distances([])

    def test_implementations_are_vectorized(self) -> None:
        for name in ("standardize_columns", "pairwise_distances", "one_hot", "scale_channels"):
            source = textwrap.dedent(inspect.getsource(getattr(self.module, name)))
            tree = ast.parse(source)
            forbidden = (ast.For, ast.While, ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)
            self.assertFalse(
                any(isinstance(node, forbidden) for node in ast.walk(tree)),
                f"{name} should use NumPy operations rather than Python loops",
            )


if __name__ == "__main__":
    unittest.main()

