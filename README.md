# Pythonlings, set 2: Fluency

This set is for someone who already knows Python's basic syntax and wants to
become comfortable *designing* with the language.  The exercises are larger
than set 1: each one asks you to implement several related behaviors, deal
with edge cases, and make choices that are checked by tests.

Python 3.11 or newer is required. Exercises 001–017 and the abstraction
capstones 026–027 use only the standard library. Exercises 018–025 explore
popular third-party libraries; install that arc in a virtual environment:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-libraries.txt
.venv/bin/python runner.py --exercise 018
```

## Working on the exercises

```sh
python3 runner.py                 # run the next unfinished exercise
python3 runner.py --exercise 004  # run one exercise
python3 runner.py --all           # run the whole set
python3 runner.py --list          # show the route and progress
python3 runner.py --reset         # clear progress only; never changes code
```

Read the module lesson, then read the docstring on every unfinished function
or class.  Replace each `raise NotImplementedError` (and any nearby placeholder
return) with your code.  You may add private helper functions.  Do not edit the
tests just to make a failure disappear—the tests are the executable version of
the contract.

If you get stuck after attempting an exercise, [HINTS.md](HINTS.md) offers two
or three graduated nudges per exercise without giving away full solutions.

Running a test directly can be useful while debugging:

```sh
python3 -m unittest tests.test_005_closures -v
```

The tests are intentionally visible.  Reading tests is an important Python
skill, and the goal is understanding rather than guessing a hidden answer.

The library lessons were designed against their current official guides:
[pytest](https://docs.pytest.org/en/stable/),
[Requests](https://requests.readthedocs.io/en/latest/),
[NumPy](https://numpy.org/doc/stable/),
[pandas](https://pandas.pydata.org/docs/),
[Pydantic](https://docs.pydantic.dev/latest/),
[Rich](https://rich.readthedocs.io/en/stable/),
[Typer](https://typer.tiangolo.com/), and
[SQLAlchemy 2](https://docs.sqlalchemy.org/en/20/).

## Route

| # | Exercise | Main ideas |
|---|---|---|
| 001 | Record pipelines | comprehensions, mappings, filtering, aggregation |
| 002 | Loop toolbox | `for`, `while`, `enumerate`, strict `zip`, `range`, nesting, control flow |
| 003 | Call signatures | positional-only, keyword-only, unpacking, sentinels |
| 004 | Functions as values | key functions, grouping, composition |
| 005 | Closures | captured state, `nonlocal`, late binding |
| 006 | Decorators | transparent wrappers, decorator factories, state |
| 007 | Lazy pipelines | iterator protocol, generator composition, laziness |
| 008 | Context managers | setup/cleanup, rollback, exception behavior |
| 009 | Dataclass models | value objects, invariants, factories, derived values |
| 010 | The data model | protocols implemented with special methods |
| 011 | Managed attributes | properties, reusable descriptors, `__set_name__` |
| 012 | Error boundaries | custom errors, validation reports, exception chaining |
| 013 | Commands and matching | enums, structural patterns, guarded cases |
| 014 | Types as design | protocols, generics, variance-friendly APIs |
| 015 | Files and JSON | `pathlib`, serialization boundaries, atomic replacement |
| 016 | SQLite repository | parameterized SQL, transactions, row mapping |
| 017 | Async orchestration | coroutines, bounded concurrency, timeouts, cancellation |
| 018 | pytest workflows | assertions, parametrization, fixtures, temporary paths, monkeypatching |
| 019 | Requests client | sessions, timeouts, status errors, JSON, streamed downloads |
| 020 | NumPy arrays | shapes, axes, broadcasting, masks, advanced indexing |
| 021 | pandas analysis | cleaning, vectorized columns, joins, grouping, time series |
| 022 | Pydantic models | parsing, field/model validators, nested models, serialization |
| 023 | Rich terminal UI | consoles, tables, styled text, progress displays |
| 024 | Typer CLI | commands, arguments, options, validation, CLI testing |
| 025 | SQLAlchemy ORM | mapped classes, relationships, sessions, select and aggregation |
| 026 | Fluent pipelines | generic classes, lazy composition, fluent APIs, operator protocols |
| 027 | Layered stores | structural protocols, adapters, generic composition, cached absence |

Exercises 001–008 develop fluency with values and control flow. Exercises
009–014 focus on interfaces and Python's object model. Exercises 015–017 put
those skills at real I/O boundaries. Exercises 018–025 then apply that Python
foundation to widely used ecosystem tools.  The library exercises teach the
underlying model and boundary decisions, not merely a sequence of API calls.
Exercises 026–027 are design capstones: they combine earlier mechanisms into
small abstractions whose pieces remain independently replaceable and testable.

## A useful learning loop

1. Predict the failure before running the test.
2. Implement the smallest complete behavior, not a special case for one test.
3. Run the focused exercise and read the first traceback from the bottom up.
4. Add one small test of your own for an edge case you nearly missed.
5. After it passes, reread your code and simplify names or control flow.
