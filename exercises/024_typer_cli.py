"""024 — Command-line applications with Typer

Typer derives a CLI from annotated Python functions.  Function parameters
become arguments or options, decorators register subcommands, normal return
values remain ordinary Python concerns, and `typer.echo`/`typer.Exit` define the
terminal boundary.  An explicit `Typer` app is easy to invoke in tests.

Complete a small JSON-backed task CLI.  File loading and saving are supplied so
you can focus on command design, validation, repeatable options, exit codes,
and keeping behavior consistent across subcommands.  Tests invoke the app in
process with Typer's `CliRunner`; no shell subprocess is needed.
"""
from __future__ import annotations

from pathlib import Path
import json
from typing import Annotated

import typer


app = typer.Typer(no_args_is_help=True, help="Manage a small task list.")


def _load(path: Path) -> list[dict[str, object]]:
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("task file must contain a list")
    return data


def _save(path: Path, tasks: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(tasks, indent=2) + "\n", encoding="utf-8")


@app.command()
def add(
    title: Annotated[str, typer.Argument(help="Task title")],
    path: Annotated[Path, typer.Option("--file", "-f", help="Task JSON file")] = Path("tasks.json"),
    tags: Annotated[list[str] | None, typer.Option("--tag", help="Repeat for multiple tags")] = None,
) -> None:
    """Add one task.

    Strip title and reject a blank with `typer.BadParameter("title must not be
    blank", param_hint="title")`.  Normalize tags by stripping/lowercasing,
    dropping blanks and duplicates while preserving order.  The new id is one
    more than the largest existing integer id, or 1.  Save fields in order: id,
    title, tags, done=False.  Echo `Added <id>: <title>`.
    """
    raise NotImplementedError


@app.command("list")
def list_tasks(
    path: Annotated[Path, typer.Option("--file", "-f", help="Task JSON file")] = Path("tasks.json"),
    status: Annotated[str | None, typer.Option("--status", help="open or done")] = None,
) -> None:
    """Print tasks as `<id> [ ] <title>` or `<id> [x] <title>`.

    Preserve file order.  Case-insensitively accept status `open` or `done` and
    filter accordingly.  Any other value raises
    `typer.BadParameter("status must be open or done", param_hint="status")`.
    Echo `No tasks.` when no rows match.
    """
    raise NotImplementedError


@app.command()
def complete(
    task_id: Annotated[int, typer.Argument(min=1, help="Task id")],
    path: Annotated[Path, typer.Option("--file", "-f", help="Task JSON file")] = Path("tasks.json"),
) -> None:
    """Mark one task done and echo `Completed <id>: <title>`.

    If absent, write `Task <id> not found.` to stderr and raise typer.Exit(1).
    Save only after finding the task.
    """
    raise NotImplementedError


if __name__ == "__main__":
    app()
