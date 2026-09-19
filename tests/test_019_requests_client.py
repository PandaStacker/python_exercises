from __future__ import annotations

from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock

import requests

from tests.support import load_exercise


class RequestsClientTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_exercise("019_requests_client.py")

    def make_client(self, responses):
        session = Mock(spec=requests.Session)
        session.get.side_effect = responses
        return self.module.ApiClient("https://api.example.test/v1", "secret", session=session, timeout=2), session

    def test_get_json_builds_a_complete_request(self) -> None:
        response = Mock()
        response.json.return_value = {"ok": True}
        client, session = self.make_client([response])
        self.assertEqual(client.get_json("status", params={"full": 1}), {"ok": True})
        session.get.assert_called_once_with(
            "https://api.example.test/v1/status",
            params={"full": 1},
            headers={"Accept": "application/json", "Authorization": "Bearer secret"},
            timeout=2,
        )
        response.raise_for_status.assert_called_once_with()

    def test_get_json_translates_status_and_json_errors(self) -> None:
        failed = Mock()
        original = requests.HTTPError("503")
        failed.raise_for_status.side_effect = original
        client, _ = self.make_client([failed])
        with self.assertRaisesRegex(self.module.ApiError, r"GET .* failed") as caught:
            client.get_json("status")
        self.assertIs(caught.exception.__cause__, original)

        invalid = Mock()
        invalid.json.side_effect = ValueError("bad JSON")
        client, _ = self.make_client([invalid])
        with self.assertRaisesRegex(self.module.ApiError, "returned invalid JSON") as caught:
            client.get_json("status")
        self.assertIsInstance(caught.exception.__cause__, ValueError)

    def test_paginated_items_are_lazy_and_params_only_apply_first(self) -> None:
        first, second = Mock(), Mock()
        first.json.return_value = {"items": [{"id": 1}, {"id": 2}], "next": "items?page=2"}
        second.json.return_value = {"items": [{"id": 3}], "next": None}
        client, session = self.make_client([first, second])
        items = client.iter_items("items", params={"limit": 2})
        self.assertEqual(session.get.call_count, 0)
        self.assertEqual(next(items), {"id": 1})
        self.assertEqual(list(items), [{"id": 2}, {"id": 3}])
        self.assertEqual(session.get.call_args_list[0].kwargs["params"], {"limit": 2})
        self.assertIsNone(session.get.call_args_list[1].kwargs["params"])

    def test_invalid_page_is_rejected(self) -> None:
        response = Mock()
        response.json.return_value = {"items": [1], "next": None}
        client, _ = self.make_client([response])
        with self.assertRaisesRegex(self.module.ApiError, "^invalid page$"):
            list(client.iter_items("items"))

    def test_download_streams_nonempty_chunks(self) -> None:
        response = Mock()
        response.iter_content.return_value = [b"abc", b"", b"de"]
        client, session = self.make_client([response])
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "download.bin"
            self.assertEqual(client.download("files/1", path, chunk_size=3), 5)
            self.assertEqual(path.read_bytes(), b"abcde")
        self.assertTrue(session.get.call_args.kwargs["stream"])
        response.iter_content.assert_called_once_with(chunk_size=3)

    def test_timeout_and_chunk_size_validation(self) -> None:
        with self.assertRaises(ValueError):
            self.module.ApiClient("https://x.test", "token", timeout=0)
        client, session = self.make_client([])
        with self.assertRaises(ValueError):
            client.download("x", "unused", chunk_size=0)
        session.get.assert_not_called()


if __name__ == "__main__":
    unittest.main()
