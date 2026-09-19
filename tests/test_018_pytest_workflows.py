from __future__ import annotations

import ast
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "exercises" / "018_pytest_workflows.py"


class PytestWorkflowTests(unittest.TestCase):
    def test_learner_pytest_suite_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", str(SOURCE), "-q"],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertRegex(result.stdout, r"9 passed|[1-9][0-9]+ passed")

    def test_required_pytest_features_remain_present(self) -> None:
        tree = ast.parse(SOURCE.read_text(encoding="utf-8"))
        attributes = {
            node.attr
            for node in ast.walk(tree)
            if isinstance(node, ast.Attribute)
        }
        self.assertIn("fixture", attributes)
        self.assertIn("parametrize", attributes)
        self.assertIn("raises", attributes)
        argument_names = {
            argument.arg
            for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            for argument in node.args.args
        }
        self.assertIn("tmp_path", argument_names)
        self.assertIn("monkeypatch", argument_names)


if __name__ == "__main__":
    unittest.main()

