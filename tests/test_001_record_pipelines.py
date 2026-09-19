from __future__ import annotations

import copy
import unittest

from tests.support import load_exercise


class RecordPipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_exercise("001_record_pipelines.py")

    def test_pipeline_normalizes_filters_and_summarizes(self) -> None:
        records = [
            {"name": "  Ada Lovelace ", "email": " ADA@Example.COM ", "tags": [" Math ", "python", "MATH", ""]},
            {"name": "Grace Hopper", "email": "Grace@Example.com", "tags": ("Navy", "COBOL")},
            {"name": "Retired User", "email": "old@example.com", "active": False, "tags": ["history"]},
            {"name": "Lin", "email": "lin@example.com"},
        ]
        original = copy.deepcopy(records)
        users = self.module.normalize_users(records)
        self.assertEqual(records, original, "normalize_users must not mutate its input")
        self.assertEqual(users, [
            {"name": "Ada Lovelace", "email": "ada@example.com", "tags": ["math", "python"]},
            {"name": "Grace Hopper", "email": "grace@example.com", "tags": ["cobol", "navy"]},
            {"name": "Lin", "email": "lin@example.com", "tags": []},
        ])
        indexed = self.module.index_by_email(users)
        self.assertIs(indexed["ada@example.com"], users[0])
        self.assertEqual(self.module.count_tags(users), {"cobol": 1, "math": 1, "navy": 1, "python": 1})

    def test_only_literal_false_is_inactive(self) -> None:
        records = [{"name": "Zero", "email": "z@x.test", "active": 0}]
        self.assertEqual(len(self.module.normalize_users(records)), 1)

    def test_duplicate_email_has_a_useful_error(self) -> None:
        users = [{"email": "same@example.com"}, {"email": "same@example.com"}]
        with self.assertRaisesRegex(ValueError, r"^duplicate email: same@example\.com$"):
            self.module.index_by_email(users)


if __name__ == "__main__":
    unittest.main()

