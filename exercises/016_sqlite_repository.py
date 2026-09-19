"""016 — A transactional SQLite repository

SQLite is part of Python's standard library and is ideal for learning database
boundaries.  SQL selects rows; Python maps rows into domain objects.  Values
must go through `?` placeholders—never string formatting—so quotes and hostile
text remain data rather than becoming SQL.

Transactions make several writes one unit.  Commit after a successful block;
on an exception, roll back and re-raise it.  The repository does not own the
connection and must not close it.
"""
from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
import sqlite3


@dataclass(frozen=True, slots=True)
class Task:
    id: int
    title: str
    done: bool


class TaskRepository:
    """Persistence operations over a caller-owned SQLite connection."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        raise NotImplementedError

    def create_schema(self) -> None:
        """Create a tasks table if absent.

        It has an auto-incrementing integer primary key, non-null title, and a
        non-null integer done flag defaulting to zero.  Do not commit here.
        """
        raise NotImplementedError

    def add(self, title: str) -> Task:
        """Strip and insert a title, returning its new Task with done False.

        Raise `ValueError("title must not be blank")` before SQL for a blank
        title.  Use the cursor's `lastrowid`.  Do not commit here.
        """
        raise NotImplementedError

    def get(self, task_id: int) -> Task | None:
        """Return one mapped Task or None."""
        raise NotImplementedError

    def list(self, *, done: bool | None = None) -> list[Task]:
        """Return tasks ordered by id, optionally filtering by done state."""
        raise NotImplementedError

    def set_done(self, task_id: int, done: bool = True) -> bool:
        """Update one task and return whether a row existed."""
        raise NotImplementedError

    def delete(self, task_id: int) -> bool:
        """Delete one task and return whether a row existed."""
        raise NotImplementedError

    @contextmanager
    def transaction(self) -> Iterator[TaskRepository]:
        """Begin a transaction, yield self, then commit or roll back.

        Reject nesting or an already active connection transaction with
        `RuntimeError("transaction already active")`.  Re-raise the exact
        exception from a failed block after rolling back.
        """
        raise NotImplementedError
        yield self

