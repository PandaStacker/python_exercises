"""023 — Terminal interfaces with Rich

Rich separates content from rendering.  `Text` carries styled spans, `Table`
is a renderable assembled from columns and rows, and `Console` decides where
and how to render it.  Passing a Console instead of constructing one deep in a
function makes output testable and lets callers choose color or file targets.

Progress is also a context-managed renderable.  Create the progress display,
add one task with a total, perform work, and advance after each completed item.
Do not print ANSI codes yourself; express intent through Rich objects.
"""
from __future__ import annotations

from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass
from typing import TypeVar

from rich import box
from rich.console import Console
from rich.progress import BarColumn, Progress, TaskProgressColumn, TextColumn
from rich.table import Table
from rich.text import Text

T = TypeVar("T")
R = TypeVar("R")


@dataclass(frozen=True, slots=True)
class Task:
    id: int
    title: str
    owner: str
    done: bool = False


def status_text(done: bool) -> Text:
    """Return `✓ done` styled green, or `• open` styled yellow."""
    raise NotImplementedError


def build_task_table(tasks: Iterable[Task]) -> Table:
    """Build a `Tasks` table using `box.SIMPLE`.

    Add columns `ID` (right-justified), `Task`, `Owner`, and `Status`.  Add one
    row per task in input order.  Convert ids to strings and use status_text for
    the final cell.
    """
    raise NotImplementedError


def render_dashboard(tasks: Sequence[Task], console: Console) -> None:
    """Print the task table followed by a bold summary.

    The summary text is `<done>/<total> complete`; construct it as a `Text`
    object with style `bold` and pass it to `console.print`.
    """
    raise NotImplementedError


def process_with_progress(
    items: Sequence[T], worker: Callable[[T], R], console: Console
) -> list[R]:
    """Process items in order while advancing a Rich Progress task.

    Construct `Progress` with a description TextColumn, BarColumn,
    TaskProgressColumn, and the supplied console.  Use it as a context manager,
    add task description `Processing` with total len(items), call worker once
    per item, append results, and advance the task once after each success.
    If worker raises, let the error propagate and do not advance that item.
    """
    raise NotImplementedError


if __name__ == "__main__":
    print("--- Testing rich terminal ---")
    try:
        console = Console()
        tasks = [Task(1, "Fix bug", "Alice", False)]
        render_dashboard(tasks, console)
    except Exception as e:
        print(f"Error: {e!r}")
