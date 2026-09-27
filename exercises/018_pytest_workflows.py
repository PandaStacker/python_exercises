"""018 — Testing effectively with pytest

pytest uses ordinary `assert` statements and rewrites them to show rich failure
details.  `@pytest.mark.parametrize` runs one test over a table of examples.
Fixtures provide explicit setup through function arguments; built-in fixtures
such as `tmp_path` and `monkeypatch` isolate filesystem and environment state.
`pytest.raises` checks both exception type and message.

Unlike the earlier exercises, the production functions below are complete.
Your job is to write the tests.  Replace every unfinished test body and fixture.
The outer Pythonlings test checks that this module's own pytest suite passes and
that you genuinely used the requested pytest features.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import pytest


def parse_bool(text: str) -> bool:
    normalized = text.strip().casefold()
    if normalized in {"yes", "true", "1", "on"}:
        return True
    if normalized in {"no", "false", "0", "off"}:
        return False
    raise ValueError(f"not a boolean: {text}")


def endpoint_from_environment() -> str:
    endpoint = os.environ.get("APP_ENDPOINT", "https://example.test")
    if not endpoint.startswith(("http://", "https://")):
        raise ValueError("APP_ENDPOINT must be an HTTP URL")
    return endpoint.rstrip("/")


def write_report(path: Path, rows: list[dict[str, object]]) -> None:
    path.write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")


@pytest.fixture
def sample_rows() -> list[dict[str, object]]:
    """Return two fresh report rows.  pytest calls this once per requesting test."""
    raise NotImplementedError


@pytest.mark.parametrize(
    "text, expected",
    [
        pytest.param("yes", True, id="yes"),
        # TODO: add at least five more cases covering whitespace, case, and
        # both numeric spellings.
    ],
)
def test_parse_bool_valid_values(text: str, expected: bool) -> None:
    """Assert that parse_bool(text) is the exact expected Boolean."""
    raise NotImplementedError


def test_parse_bool_rejects_unknown_text() -> None:
    """Use pytest.raises(..., match=...) to check `maybe` and its full message."""
    raise NotImplementedError


def test_environment_endpoint(monkeypatch: pytest.MonkeyPatch) -> None:
    """Set APP_ENDPOINT with monkeypatch and assert trailing slashes are removed."""
    raise NotImplementedError


def test_report_round_trip(tmp_path: Path, sample_rows: list[dict[str, object]]) -> None:
    """Write under tmp_path, load the JSON back, and compare it to sample_rows."""
    raise NotImplementedError


def test_fixture_is_fresh(sample_rows: list[dict[str, object]]) -> None:
    """Mutate sample_rows and assert its length is now three.

    If the round-trip test still sees two rows, you have demonstrated the
    fixture's function scope rather than sharing global mutable state.
    """
    raise NotImplementedError


if __name__ == "__main__":
    print("--- Running pytest ---")
    import sys
    sys.exit(pytest.main(["-v", __file__]))
