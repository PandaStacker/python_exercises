from __future__ import annotations

import sqlite3
import unittest

from tests.support import load_exercise


class SQLiteRepositoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_exercise("016_sqlite_repository.py")

    def setUp(self) -> None:
        self.connection = sqlite3.connect(":memory:")
        self.repo = self.module.TaskRepository(self.connection)
        self.repo.create_schema()
        self.connection.commit()

    def tearDown(self) -> None:
        self.connection.close()

    def test_crud_and_row_mapping(self) -> None:
        first = self.repo.add("  learn SQL ")
        second = self.repo.add("write tests")
        self.assertEqual(first, self.module.Task(1, "learn SQL", False))
        self.assertEqual(self.repo.get(second.id), second)
        self.assertIsNone(self.repo.get(999))
        self.assertTrue(self.repo.set_done(first.id))
        self.assertFalse(self.repo.set_done(999))
        self.assertEqual(self.repo.list(done=True), [self.module.Task(1, "learn SQL", True)])
        self.assertEqual(self.repo.list(done=False), [second])
        self.assertTrue(self.repo.delete(second.id))
        self.assertFalse(self.repo.delete(second.id))

    def test_values_are_parameterized(self) -> None:
        hostile = "Robert'); DROP TABLE tasks;--"
        task = self.repo.add(hostile)
        self.assertEqual(task.title, hostile)
        self.assertEqual(self.repo.list(), [task])

    def test_blank_title_is_rejected_without_writing(self) -> None:
        with self.assertRaisesRegex(ValueError, "^title must not be blank$"):
            self.repo.add("  ")
        self.assertEqual(self.repo.list(), [])

    def test_transaction_commits_success_and_rolls_back_failure(self) -> None:
        with self.repo.transaction() as entered:
            self.assertIs(entered, self.repo)
            entered.add("kept")
        self.assertFalse(self.connection.in_transaction)
        self.assertEqual([task.title for task in self.repo.list()], ["kept"])

        with self.assertRaisesRegex(RuntimeError, "boom"):
            with self.repo.transaction():
                self.repo.add("discarded")
                raise RuntimeError("boom")
        self.assertFalse(self.connection.in_transaction)
        self.assertEqual([task.title for task in self.repo.list()], ["kept"])

    def test_transaction_rejects_nesting_and_does_not_close_connection(self) -> None:
        with self.repo.transaction():
            with self.assertRaisesRegex(RuntimeError, "transaction already active"):
                with self.repo.transaction():
                    pass
        self.connection.execute("SELECT 1").fetchone()


if __name__ == "__main__":
    unittest.main()

