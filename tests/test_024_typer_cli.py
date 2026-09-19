from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from typer.testing import CliRunner

from tests.support import load_exercise


class TyperCliTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_exercise("024_typer_cli.py")
        cls.runner = CliRunner()

    def test_add_normalizes_repeatable_tags_and_increments_ids(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tasks.json"
            first = self.runner.invoke(self.module.app, ["add", "  Learn Typer ", "-f", str(path), "--tag", " CLI ", "--tag", "cli", "--tag", "Python"])
            second = self.runner.invoke(self.module.app, ["add", "Write tests", "-f", str(path)])
            self.assertEqual(first.exit_code, 0, first.output)
            self.assertIn("Added 1: Learn Typer", first.output)
            self.assertIn("Added 2: Write tests", second.output)
            self.assertEqual(
                json.loads(path.read_text()),
                [
                    {"id": 1, "title": "Learn Typer", "tags": ["cli", "python"], "done": False},
                    {"id": 2, "title": "Write tests", "tags": [], "done": False},
                ],
            )

    def test_blank_title_and_bad_status_are_cli_errors(self) -> None:
        blank = self.runner.invoke(self.module.app, ["add", "   "])
        self.assertNotEqual(blank.exit_code, 0)
        self.assertIn("title must not be blank", blank.output)
        bad_status = self.runner.invoke(self.module.app, ["list", "--status", "later"])
        self.assertNotEqual(bad_status.exit_code, 0)
        self.assertIn("status must be open or done", bad_status.output)

    def test_list_filter_and_complete_workflow(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tasks.json"
            path.write_text(json.dumps([
                {"id": 3, "title": "Open task", "tags": [], "done": False},
                {"id": 8, "title": "Old task", "tags": [], "done": True},
            ]))
            open_result = self.runner.invoke(self.module.app, ["list", "-f", str(path), "--status", "OPEN"])
            self.assertEqual(open_result.exit_code, 0, open_result.output)
            self.assertIn("3 [ ] Open task", open_result.output)
            self.assertNotIn("Old task", open_result.output)

            completed = self.runner.invoke(self.module.app, ["complete", "3", "-f", str(path)])
            self.assertEqual(completed.exit_code, 0, completed.output)
            self.assertIn("Completed 3: Open task", completed.output)
            tasks = json.loads(path.read_text())
            self.assertTrue(tasks[0]["done"])

    def test_missing_complete_uses_exit_code_one_without_writing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tasks.json"
            path.write_text("[]\n")
            result = self.runner.invoke(self.module.app, ["complete", "4", "-f", str(path)])
            self.assertEqual(result.exit_code, 1)
            self.assertIn("Task 4 not found.", result.output)
            self.assertEqual(path.read_text(), "[]\n")

    def test_help_exposes_commands_and_options(self) -> None:
        result = self.runner.invoke(self.module.app, ["--help"])
        self.assertEqual(result.exit_code, 0, result.output)
        for command in ("add", "list", "complete"):
            self.assertIn(command, result.output)
        add_help = self.runner.invoke(self.module.app, ["add", "--help"])
        self.assertIn("--tag", add_help.output)
        self.assertIn("--file", add_help.output)


if __name__ == "__main__":
    unittest.main()

