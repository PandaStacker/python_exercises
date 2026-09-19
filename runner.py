#!/usr/bin/env python3
"""Progress-aware test runner for Pythonlings set 2."""
from __future__ import annotations

import argparse
import ast
import io
import importlib.util
import json
import subprocess
import sys
import tokenize
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROGRESS_FILE = ROOT / ".progress.json"


@dataclass(frozen=True)
class Exercise:
    number: str
    slug: str
    title: str
    dependencies: tuple[str, ...] = ()

    @property
    def source(self) -> Path:
        return ROOT / "exercises" / f"{self.number}_{self.slug}.py"

    @property
    def test_module(self) -> str:
        return f"tests.test_{self.number}_{self.slug}"


EXERCISES = [
    Exercise("001", "record_pipelines", "Record pipelines"),
    Exercise("002", "loop_toolbox", "The loop toolbox"),
    Exercise("003", "call_signatures", "Call signatures and unpacking"),
    Exercise("004", "functions_as_values", "Functions as values"),
    Exercise("005", "closures", "Closures and captured state"),
    Exercise("006", "decorators", "Production-quality decorators"),
    Exercise("007", "lazy_pipelines", "Lazy iterator pipelines"),
    Exercise("008", "context_managers", "Context managers and rollback"),
    Exercise("009", "dataclass_models", "Dataclass domain models"),
    Exercise("010", "data_model", "Python's data model"),
    Exercise("011", "descriptors", "Managed attributes and descriptors"),
    Exercise("012", "error_boundaries", "Errors at system boundaries"),
    Exercise("013", "pattern_matching", "Enums and structural matching"),
    Exercise("014", "typing_protocols", "Protocols and generics"),
    Exercise("015", "files_and_json", "Files and JSON persistence"),
    Exercise("016", "sqlite_repository", "A transactional SQLite repository"),
    Exercise("017", "async_orchestration", "Async orchestration"),
    Exercise("018", "pytest_workflows", "Testing effectively with pytest", ("pytest",)),
    Exercise("019", "requests_client", "HTTP clients with Requests", ("requests",)),
    Exercise("020", "numpy_arrays", "Vectorized arrays with NumPy", ("numpy",)),
    Exercise("021", "pandas_analysis", "Tabular analysis with pandas", ("pandas",)),
    Exercise("022", "pydantic_models", "Validation with Pydantic", ("pydantic",)),
    Exercise("023", "rich_terminal", "Terminal interfaces with Rich", ("rich",)),
    Exercise("024", "typer_cli", "Command-line applications with Typer", ("typer",)),
    Exercise("025", "sqlalchemy_orm", "Database mapping with SQLAlchemy", ("sqlalchemy",)),
    Exercise("026", "fluent_pipeline", "Designing a fluent lazy abstraction"),
    Exercise("027", "layered_stores", "Protocols, adapters, and layered stores"),
]


def load_progress() -> set[str]:
    try:
        value = json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
        return set(value) if isinstance(value, list) else set()
    except (FileNotFoundError, json.JSONDecodeError):
        return set()


def save_progress(done: set[str]) -> None:
    PROGRESS_FILE.write_text(
        json.dumps(sorted(done), indent=2) + "\n", encoding="utf-8"
    )


def lesson_for(exercise: Exercise) -> str:
    """Read the leading docstring even when the learner's code will not import."""
    source = exercise.source.read_text(encoding="utf-8")
    tokens = tokenize.generate_tokens(io.StringIO(source).readline)
    try:
        first = next(token for token in tokens if token.type not in {tokenize.NL, tokenize.COMMENT})
        if first.type == tokenize.STRING:
            value = ast.literal_eval(first.string)
            return value.strip() if isinstance(value, str) else ""
    except (StopIteration, SyntaxError, tokenize.TokenError):
        pass
    return ""


def check(exercise: Exercise) -> tuple[bool, str]:
    missing = [name for name in exercise.dependencies if importlib.util.find_spec(name) is None]
    if missing:
        names = ", ".join(missing)
        return False, (
            f"Missing exercise dependencies: {names}\n"
            f"Install them with:\n  {sys.executable} -m pip install -r "
            "requirements-libraries.txt\n"
        )
    result = subprocess.run(
        [sys.executable, "-m", "unittest", exercise.test_module, "-v"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    return result.returncode == 0, result.stdout


def choose_exercises(args: argparse.Namespace, done: set[str]) -> list[Exercise]:
    if args.exercise:
        matches = [item for item in EXERCISES if item.number == args.exercise]
        if not matches:
            raise ValueError(f"unknown exercise: {args.exercise}")
        return matches
    if args.all:
        return EXERCISES
    return [next((item for item in EXERCISES if item.number not in done), EXERCISES[-1])]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--all", action="store_true", help="run every exercise")
    parser.add_argument("--list", action="store_true", help="show route and progress")
    parser.add_argument("--exercise", metavar="NUMBER", help="run one exercise")
    parser.add_argument("--reset", action="store_true", help="forget recorded progress")
    args = parser.parse_args()

    if args.reset:
        PROGRESS_FILE.unlink(missing_ok=True)
        print("Progress reset. Your exercise files were not changed.")
        return 0

    done = load_progress()
    if args.list:
        for exercise in EXERCISES:
            mark = "✓" if exercise.number in done else "·"
            print(f"{mark} {exercise.number}  {exercise.title}")
        return 0

    try:
        selected = choose_exercises(args, done)
    except ValueError as error:
        parser.error(str(error))

    failures = 0
    for exercise in selected:
        print(f"\n== {exercise.number}: {exercise.title} ==")
        print(lesson_for(exercise))
        print()
        passed, output = check(exercise)
        print(output.rstrip())
        if passed:
            done.add(exercise.number)
            save_progress(done)
            print("Passed.")
        else:
            failures += 1
            print("Not passed yet.")
            if not args.all:
                break
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
