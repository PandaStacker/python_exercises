"""015 — Files and JSON persistence

Files are a boundary between Python's rich objects and a small set of JSON
types.  Make that conversion explicit instead of spreading dictionary access
through the program.  Validate while reading so the rest of the program can
trust its `Task` objects.

Saving through a sibling temporary file and then replacing the destination
avoids leaving a half-written main file if writing fails.  `Path.replace` is an
atomic operation on normal local filesystems when source and destination share
a filesystem.  A `finally` block should clean up a leftover temporary file.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, Iterable, Mapping


@dataclass(frozen=True, slots=True)
class Task:
    id: int
    title: str
    done: bool = False
    tags: tuple[str, ...] = ()


class TaskFileError(ValueError):
    """A task file could not be decoded or validated."""


def task_from_dict(data: Mapping[str, Any]) -> Task:
    """Validate and convert one JSON-shaped mapping.

    Require exactly the keys `id`, `title`, `done`, and `tags`.  `id` is a
    positive int (not bool), title is a non-blank string which is stripped,
    done is a bool, and tags is a list of strings.  Strip tags, reject blanks,
    and store them as a tuple.  Raise `TaskFileError` with a short explanation
    for any invalid input; exact wording is left to you.
    """
    raise NotImplementedError


def task_to_dict(task: Task) -> dict[str, Any]:
    """Return a JSON-shaped dict with id, title, done, and tags in that order."""
    raise NotImplementedError


def load_tasks(path: str | Path) -> list[Task]:
    """Load a UTF-8 JSON task list; return [] when the path does not exist.

    The JSON root must be a list and each element must be an object.  Translate
    JSON decoding errors to `TaskFileError("invalid JSON")` using exception
    chaining.  Translate a bad element to
    `TaskFileError("invalid task at index <n>: <reason>")`, chaining the
    TaskFileError raised by `task_from_dict`.
    """
    raise NotImplementedError


def save_tasks(path: str | Path, tasks: Iterable[Task]) -> None:
    """Atomically save tasks as UTF-8 JSON.

    Create missing parent directories.  Write to `<filename>.tmp` in the same
    directory using `json.dump(..., indent=2)`, append one newline, then replace
    the requested path.  Always remove a leftover temporary file on failure.
    """
    raise NotImplementedError

