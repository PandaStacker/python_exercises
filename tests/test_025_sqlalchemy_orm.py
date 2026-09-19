from __future__ import annotations

import unittest

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from tests.support import load_exercise


class SQLAlchemyOrmTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_exercise("025_sqlalchemy_orm.py")

    def setUp(self) -> None:
        self.engine = create_engine("sqlite+pysqlite:///:memory:")
        self.module.Base.metadata.create_all(self.engine)
        self.session = Session(self.engine)

    def tearDown(self) -> None:
        self.session.close()
        self.engine.dispose()

    def test_create_project_builds_relationship_and_flushes_ids(self) -> None:
        project = self.module.create_project(self.session, " Core ", [" First ", "Second"])
        self.assertIsNotNone(project.id)
        self.assertEqual(project.name, "Core")
        self.assertEqual([issue.title for issue in project.issues], ["First", "Second"])
        self.assertTrue(all(issue.id is not None for issue in project.issues))
        self.assertTrue(all(issue.project is project for issue in project.issues))
        self.assertTrue(self.session.in_transaction())

    def test_validation_happens_before_session_mutation(self) -> None:
        with self.assertRaises(ValueError):
            self.module.create_project(self.session, " ", ["valid"])
        self.assertEqual(list(self.session.new), [])
        with self.assertRaises(ValueError):
            self.module.create_project(self.session, "valid", ["ok", " "])
        self.assertEqual(list(self.session.new), [])

    def seed(self):
        beta = self.module.create_project(self.session, "Beta", ["B open", "B done"])
        alpha = self.module.create_project(self.session, "Alpha", ["A open"])
        empty = self.module.create_project(self.session, "Empty")
        beta.issues[1].done = True
        self.session.flush()
        return alpha, beta, empty

    def test_query_filters_and_orders_open_issues(self) -> None:
        alpha, beta, _ = self.seed()
        self.assertEqual([issue.title for issue in self.module.open_issues(self.session)], ["A open", "B open"])
        self.assertEqual([issue.title for issue in self.module.open_issues(self.session, project_name="Beta")], ["B open"])
        self.assertEqual(self.module.open_issues(self.session, project_name="Missing"), [])

    def test_close_and_aggregate(self) -> None:
        alpha, beta, empty = self.seed()
        self.assertEqual(
            self.module.project_summaries(self.session),
            [("Alpha", 1, 1), ("Beta", 2, 1), ("Empty", 0, 0)],
        )
        self.assertTrue(self.module.close_issue(self.session, alpha.issues[0].id))
        self.assertFalse(self.module.close_issue(self.session, 9999))
        self.assertEqual(self.module.project_summaries(self.session)[0], ("Alpha", 1, 0))

    def test_delete_uses_relationship_cascade(self) -> None:
        _, beta, _ = self.seed()
        issue_ids = [issue.id for issue in beta.issues]
        self.assertTrue(self.module.delete_project(self.session, beta.id))
        self.session.flush()
        self.assertIsNone(self.session.get(self.module.Project, beta.id))
        remaining = self.session.scalars(select(self.module.Issue).where(self.module.Issue.id.in_(issue_ids))).all()
        self.assertEqual(remaining, [])
        self.assertFalse(self.module.delete_project(self.session, 9999))


if __name__ == "__main__":
    unittest.main()
