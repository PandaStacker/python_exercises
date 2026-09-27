"""019 — HTTP clients with Requests

Requests turns HTTP exchanges into Python objects, but production clients must
still define boundaries: reuse a `Session`, always set a timeout, treat bad
status codes as errors, validate decoded JSON, and stream large bodies instead
of loading them all at once.

Dependency injection keeps these behaviors testable.  Accept a caller-supplied
session and let tests provide a fake—none of this exercise's tests use the
network.  Catch Requests errors only where you can add useful application
context, and preserve their cause with `raise ... from ...`.
"""
from __future__ import annotations

from collections.abc import Iterator, Mapping
from pathlib import Path
from typing import Any
from urllib.parse import urljoin

import requests


class ApiError(RuntimeError):
    pass


class ApiClient:
    def __init__(
        self,
        base_url: str,
        token: str,
        *,
        session: requests.Session | None = None,
        timeout: float = 5.0,
    ) -> None:
        """Store a slash-terminated base URL, token, session, and timeout.

        Create `requests.Session()` only when no session is supplied.  Require
        timeout > 0.  Do not put authorization in mutable session-wide headers;
        build request headers in `_headers` instead.
        """
        raise NotImplementedError

    def _headers(self) -> dict[str, str]:
        """Return fresh Accept JSON and Bearer Authorization headers."""
        raise NotImplementedError

    def get_json(
        self, path: str, *, params: Mapping[str, object] | None = None
    ) -> dict[str, Any]:
        """GET one endpoint, check status, and return a JSON object.

        Pass params, headers, and timeout explicitly.  Translate any
        `requests.RequestException` to `ApiError("GET <url> failed")` with
        chaining.  Translate JSON decoding failure or a non-dict JSON value to
        `ApiError("GET <url> returned invalid JSON")` with chaining when a
        decoding exception exists.
        """
        raise NotImplementedError

    def iter_items(
        self, path: str, *, params: Mapping[str, object] | None = None
    ) -> Iterator[dict[str, Any]]:
        """Lazily follow object-shaped pagination responses.

        Each response is `{"items": [objects...], "next": str | None}`.  Yield
        every item and fetch `next` as the following path.  Validate this shape,
        raising `ApiError("invalid page")` for malformed data.  Apply `params`
        only to the first request.
        """
        raise NotImplementedError
        yield

    def download(self, path: str, destination: str | Path, *, chunk_size: int = 8192) -> int:
        """Stream a GET body to a file and return bytes written.

        Require positive chunk_size.  Call session.get with `stream=True`,
        headers, and timeout; call raise_for_status before opening the file.
        Iterate `response.iter_content(chunk_size=chunk_size)`, skipping empty
        keep-alive chunks.  Translate RequestException as in `get_json`.
        """
        raise NotImplementedError


if __name__ == "__main__":
    print("--- Testing requests client ---")
    try:
        client = ApiClient("https://example.com/", "test_token")
        print("Headers created:")
        # Should raise NotImplementedError if not done
        print(client._headers())
    except Exception as e:
        print(f"Error: {e!r}")
