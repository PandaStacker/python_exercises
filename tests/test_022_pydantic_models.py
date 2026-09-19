from __future__ import annotations

import json
import unittest

from pydantic import ValidationError

from tests.support import load_exercise


class PydanticModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_exercise("022_pydantic_models.py")

    def valid_data(self):
        return {
            "username": " Ada_1 ",
            "password": "correct horse",
            "password_repeat": "correct horse",
            "tags": " Python, math, PYTHON, ",
            "address": {"street": " 1 Code Way ", "city": " Toronto ", "postal_code": "m5v3a8"},
        }

    def test_nested_model_normalizes_and_computes(self) -> None:
        registration = self.module.Registration.model_validate(self.valid_data())
        self.assertEqual(registration.username, "ada_1")
        self.assertEqual(registration.tags, ["python", "math"])
        self.assertEqual(registration.address.city, "Toronto")
        self.assertEqual(registration.address.postal_code, "M5V 3A8")
        self.assertEqual(registration.profile_slug, "ada_1-m5v3a8")

    def test_serialization_excludes_passwords_but_includes_computed_field(self) -> None:
        dumped = self.module.Registration.model_validate(self.valid_data()).model_dump()
        self.assertNotIn("password", dumped)
        self.assertNotIn("password_repeat", dumped)
        self.assertEqual(dumped["profile_slug"], "ada_1-m5v3a8")

    def test_field_model_and_extra_validation(self) -> None:
        cases = [
            ({**self.valid_data(), "username": "No spaces"}, "username"),
            ({**self.valid_data(), "password_repeat": "different"}, "passwords do not match"),
            ({**self.valid_data(), "address": {"street": "x", "city": "y", "postal_code": "wrong"}}, "postal_code"),
            ({**self.valid_data(), "unexpected": True}, "unexpected"),
            ({**self.valid_data(), "tags": ["ok", 3]}, "tags must be strings"),
        ]
        for data, message in cases:
            with self.subTest(message=message), self.assertRaisesRegex(ValidationError, message):
                self.module.Registration.model_validate(data)

    def test_json_adapter_parses_a_list(self) -> None:
        first = self.valid_data()
        second = {**self.valid_data(), "username": "grace", "address": None, "tags": []}
        result = self.module.parse_registrations_json(json.dumps([first, second]))
        self.assertEqual([item.username for item in result], ["ada_1", "grace"])
        self.assertEqual(result[1].profile_slug, "grace-remote")
        with self.assertRaises(ValidationError):
            self.module.parse_registrations_json("{}")


if __name__ == "__main__":
    unittest.main()

