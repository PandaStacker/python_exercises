from __future__ import annotations

import ast
import inspect
import textwrap
import unittest

from tests.support import load_exercise


class LoopToolboxTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_exercise("002_loop_toolbox.py")

    def test_enumerate(self) -> None:
        users = ({"name": name} for name in ("Ada", "Grace", "Lin"))
        self.assertEqual(self.module.numbered_names(users, 4), ["4. Ada", "5. Grace", "6. Lin"])

    def test_strict_zip_without_mutation(self) -> None:
        users = [{"name": "Ada"}, {"name": "Grace"}]
        self.assertEqual(self.module.attach_scores(users, (98, 95)), [{"name": "Ada", "score": 98}, {"name": "Grace", "score": 95}])
        self.assertEqual(users, [{"name": "Ada"}, {"name": "Grace"}])
        with self.assertRaises(ValueError):
            self.module.attach_scores(users, [100])

    def test_for_else_search(self) -> None:
        users = [{"name": "Ada", "tags": ["math"]}, {"name": "Grace", "tags": ["cobol"]}]
        self.assertIs(self.module.first_user_with_tag(iter(users), " COBOL "), users[1])
        self.assertIsNone(self.module.first_user_with_tag(users, "compiler"))

    def test_range_chunks(self) -> None:
        users = [{"id": number} for number in range(5)]
        chunks = self.module.chunk_users(users, 2)
        self.assertEqual(chunks, [[{"id": 0}, {"id": 1}], [{"id": 2}, {"id": 3}], [{"id": 4}]])
        chunks[0].append({"id": 99})
        self.assertEqual(len(users), 5)
        with self.assertRaisesRegex(ValueError, "^size must be positive$"):
            self.module.chunk_users(users, 0)

    def test_while_pagination(self) -> None:
        calls = []
        pages = {None: ([{"id": 1}], "next"), "next": (({"id": 2},), None)}
        def fetch(token):
            calls.append(token)
            return pages[token]
        self.assertEqual(self.module.collect_pages(fetch), [{"id": 1}, {"id": 2}])
        self.assertEqual(calls, [None, "next"])

    def test_continue_and_nested_loops(self) -> None:
        users = [
            {"name": "Ada", "active": True, "tags": ["math", "python"]},
            {"name": "Old", "active": False, "tags": ["history"]},
            {"name": "Grace", "tags": ["python", "navy"]},
        ]
        self.assertEqual(self.module.active_names(users), ["Ada", "Grace"])
        self.assertEqual(self.module.count_nested_tags(users), {"history": 1, "math": 1, "navy": 1, "python": 2})

    def test_requested_constructs_are_used(self) -> None:
        def tree(function):
            return ast.parse(textwrap.dedent(inspect.getsource(function)))
        def calls(function, name):
            return [n for n in ast.walk(tree(function)) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == name]
        self.assertTrue(calls(self.module.numbered_names, "enumerate"), "use enumerate")
        zip_calls = calls(self.module.attach_scores, "zip")
        self.assertTrue(any(any(k.arg == "strict" and isinstance(k.value, ast.Constant) and k.value.value is True for k in c.keywords) for c in zip_calls), "use strict zip")
        self.assertTrue(calls(self.module.chunk_users, "range"), "use range")
        self.assertTrue(any(isinstance(n, ast.While) for n in ast.walk(tree(self.module.collect_pages))), "use while")
        self.assertTrue(any(isinstance(n, ast.For) and n.orelse for n in ast.walk(tree(self.module.first_user_with_tag))), "use for else")
        self.assertTrue(any(isinstance(n, ast.Continue) for n in ast.walk(tree(self.module.active_names))), "use continue")
        self.assertGreaterEqual(sum(isinstance(n, ast.For) for n in ast.walk(tree(self.module.count_nested_tags))), 2)


if __name__ == "__main__":
    unittest.main()
