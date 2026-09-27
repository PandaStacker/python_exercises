"""025 — Database mapping with SQLAlchemy's ORM

SQLAlchemy maps Python classes to relational tables.  `Mapped[...]` annotations
and `mapped_column` describe columns; `relationship` connects object graphs.
A `Session` is both an identity map and a transaction boundary.  SQLAlchemy 2
queries use `select(...)`, and `session.scalars(...)` extracts mapped entities.

The mappings are supplied so this exercise can focus on useful session work:
constructing related objects, flushing generated ids, composing queries,
aggregating with an outer join, and relying on relationship cascades.  Do not
commit inside these helpers—the caller owns the transaction.
"""
from __future__ import annotations

from collections.abc import Iterable

from sqlalchemy import Boolean, ForeignKey, String, func, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    issues: Mapped[list[Issue]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Project(id={self.id!r}, name={self.name!r})"


class Issue(Base):
    __tablename__ = "issues"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    done: Mapped[bool] = mapped_column(Boolean, default=False)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    project: Mapped[Project] = relationship(back_populates="issues")

    def __repr__(self) -> str:
        return f"Issue(id={self.id!r}, title={self.title!r}, done={self.done!r})"


def create_project(session: Session, name: str, issue_titles: Iterable[str] = ()) -> Project:
    """Validate, add, and flush a Project with related Issues.

    Strip name and every title.  Reject any blank with ValueError before adding
    anything to the session.  Construct relationships through `Project.issues`,
    add only the project explicitly, call `session.flush()` so ids are assigned,
    and return it.  Do not commit.
    """
    raise NotImplementedError


def open_issues(session: Session, *, project_name: str | None = None) -> list[Issue]:
    """Select unfinished issues ordered by project name then issue id.

    Join Project so it can be ordered and optionally filter by exact project
    name.  Execute with `session.scalars(statement).all()` and return a list.
    """
    raise NotImplementedError


def close_issue(session: Session, issue_id: int) -> bool:
    """Load with `session.get`, set done True, and report whether it existed."""
    raise NotImplementedError


def project_summaries(session: Session) -> list[tuple[str, int, int]]:
    """Return `(project name, total issues, open issues)` ordered by name.

    Build one aggregate SELECT starting from Project, outer-joining Issue so
    projects with no issues remain.  Use `func.count(Issue.id)` for total and a
    filtered count whose filter is `Issue.done.is_(False)` for open issues.
    Group by project id and name.  Convert returned Row objects to plain tuples.
    """
    raise NotImplementedError


def delete_project(session: Session, project_id: int) -> bool:
    """Delete a loaded project and report whether it existed.

    The supplied relationship cascade must delete its issues when flushed.
    Do not issue a separate Issue delete and do not commit.
    """
    raise NotImplementedError


if __name__ == "__main__":
    print("--- Testing sqlalchemy orm ---")
    try:
        from sqlalchemy import create_engine
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)
        with Session(engine) as session:
            p = create_project(session, "Project 1", ["Issue 1"])
            print("Project created:", p)
    except Exception as e:
        print(f"Error: {e!r}")
