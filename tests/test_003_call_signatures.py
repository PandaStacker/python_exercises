from __future__ import annotations

import inspect
import unittest

from tests.support import load_exercise


class CallSignatureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_exercise("003_call_signatures.py")

    def test_address_and_signature_constraints(self) -> None:
        self.assertEqual(
            self.module.format_address("Ada", city="Toronto", region="ON"),
            "Ada — Toronto, ON, Canada",
        )
        self.assertEqual(
            self.module.format_address("Lin", city="Paris", country="France"),
            "Lin — Paris, France",
        )
        with self.assertRaises(TypeError):
            self.module.format_address(name="Ada", city="Toronto")
        with self.assertRaises(TypeError):
            self.module.format_address("Ada", "Toronto")

    def test_merge_precedence_and_no_mutation(self) -> None:
        base = {"theme": "light", "page_size": 10}
        team = {"page_size": 25, "locale": "en"}
        result = self.module.merge_settings(base, team, {"locale": "fr"}, theme="dark")
        self.assertEqual(result, {"theme": "dark", "page_size": 25, "locale": "fr"})
        self.assertEqual(base, {"theme": "light", "page_size": 10})
        self.assertEqual(team, {"page_size": 25, "locale": "en"})

    def test_sentinel_distinguishes_none_from_omission(self) -> None:
        profile = {"name": "Ada", "email": "a@example.com", "role": "admin"}
        result = self.module.update_profile(profile, email=None, bio="First programmer")
        self.assertEqual(
            result,
            {"name": "Ada", "email": None, "bio": "First programmer", "role": "admin"},
        )
        self.assertEqual(profile["email"], "a@example.com")

    def test_invoke_forwards_then_transforms(self) -> None:
        calls = []

        def combine(a, b, *, separator="/"):
            calls.append((a, b, separator))
            return f"{a}{separator}{b}"

        result = self.module.invoke(combine, "left", "right", separator="|", transform=str.upper)
        self.assertEqual(result, "LEFT|RIGHT")
        self.assertEqual(calls, [("left", "right", "|")])

    def test_signatures_were_not_weakened(self) -> None:
        address = inspect.signature(self.module.format_address)
        self.assertEqual(address.parameters["name"].kind, inspect.Parameter.POSITIONAL_ONLY)
        self.assertEqual(address.parameters["city"].kind, inspect.Parameter.KEYWORD_ONLY)


if __name__ == "__main__":
    unittest.main()

