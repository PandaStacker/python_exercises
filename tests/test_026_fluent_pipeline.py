from __future__ import annotations

import unittest

from tests.support import load_exercise


class FluentPipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_exercise("026_fluent_pipeline.py")

    def test_factory_is_lazy_and_pipeline_is_reusable(self) -> None:
        calls = []
        def source():
            calls.append("started")
            return iter([1, 2, 3])
        pipeline = self.module.Pipeline.from_factory(source).map(lambda n: n * 10)
        self.assertEqual(calls, [])
        self.assertEqual(list(pipeline), [10, 20, 30])
        self.assertEqual(list(pipeline), [10, 20, 30])
        self.assertEqual(calls, ["started", "started"])

    def test_operators_compose_without_intermediate_lists(self) -> None:
        seen = []
        pipeline = (
            self.module.Pipeline.of("  Ada ", "", " Grace")
            .map(str.strip)
            .where(bool)
            .flat_map(lambda name: (name, name.upper()))
            .tap(seen.append)
        )
        self.assertEqual(seen, [])
        self.assertEqual(list(pipeline), ["Ada", "ADA", "Grace", "GRACE"])
        self.assertEqual(seen, ["Ada", "ADA", "Grace", "GRACE"])

    def test_take_does_not_overconsume(self) -> None:
        consumed = []
        def values():
            for number in range(100):
                consumed.append(number)
                yield number
        result = list(self.module.Pipeline.from_factory(values).take(3))
        self.assertEqual(result, [0, 1, 2])
        self.assertEqual(consumed, [0, 1, 2])
        self.assertEqual(list(self.module.Pipeline.of(1, 2).take(0)), [])
        with self.assertRaisesRegex(ValueError, "^count must be non-negative$"):
            self.module.Pipeline.of(1).take(-1)

    def test_pipe_operator_builds_reusable_stages(self) -> None:
        clean = self.module.mapping(str.strip)
        nonempty = self.module.filtering(bool)
        result = self.module.Pipeline.of(" a ", " ", "b ") | clean | nonempty
        self.assertEqual(list(result), ["a", "b"])

    def test_reduce_is_the_explicit_eager_boundary(self) -> None:
        pipeline = self.module.Pipeline.of(1, 2, 3, 4).where(lambda n: n % 2 == 0)
        self.assertEqual(pipeline.reduce(10, lambda total, n: total + n), 16)
        self.assertEqual(self.module.Pipeline.of().reduce("seed", lambda a, b: a + b), "seed")


if __name__ == "__main__":
    unittest.main()

