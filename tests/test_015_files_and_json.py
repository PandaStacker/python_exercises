from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from tests.support import load_exercise


class FileAndJsonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_exercise("015_files_and_json.py")

    def test_conversion_validates_and_does_not_alias_tags(self) -> None:
        tags = [" work ", "urgent"]
        task = self.module.task_from_dict(
            {"id": 3, "title": "  Ship release ", "done": False, "tags": tags}
        )
        tags.append("later")
        self.assertEqual(task, self.module.Task(3, "Ship release", False, ("work", "urgent")))
        self.assertEqual(
            self.module.task_to_dict(task),
            {"id": 3, "title": "Ship release", "done": False, "tags": ["work", "urgent"]},
        )

    def test_conversion_rejects_wrong_shape_and_types(self) -> None:
        valid = {"id": 1, "title": "Task", "done": False, "tags": []}
        bad_values = [
            {**valid, "extra": 1},
            {key: value for key, value in valid.items() if key != "done"},
            {**valid, "id": True},
            {**valid, "title": " "},
            {**valid, "done": 0},
            {**valid, "tags": ["ok", " "]},
        ]
        for value in bad_values:
            with self.subTest(value=value), self.assertRaises(self.module.TaskFileError):
                self.module.task_from_dict(value)

    def test_round_trip_and_missing_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "nested" / "tasks.json"
            tasks = [
                self.module.Task(1, "One", False, ("a",)),
                self.module.Task(2, "Two", True, ()),
            ]
            self.assertEqual(self.module.load_tasks(path), [])
            self.module.save_tasks(path, (task for task in tasks))
            self.assertEqual(self.module.load_tasks(path), tasks)
            self.assertTrue(path.read_text(encoding="utf-8").endswith("\n"))
            self.assertFalse(path.with_name("tasks.json.tmp").exists())

    def test_load_errors_preserve_context(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tasks.json"
            path.write_text("{not json", encoding="utf-8")
            with self.assertRaisesRegex(self.module.TaskFileError, "^invalid JSON$") as caught:
                self.module.load_tasks(path)
            self.assertIsInstance(caught.exception.__cause__, json.JSONDecodeError)

            path.write_text(
                json.dumps([{"id": 0, "title": "bad", "done": False, "tags": []}]),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(self.module.TaskFileError, "^invalid task at index 0:") as caught:
                self.module.load_tasks(path)
            self.assertIsInstance(caught.exception.__cause__, self.module.TaskFileError)

    def test_json_root_must_be_a_list(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tasks.json"
            path.write_text("{}", encoding="utf-8")
            with self.assertRaises(self.module.TaskFileError):
                self.module.load_tasks(path)


if __name__ == "__main__":
    unittest.main()

