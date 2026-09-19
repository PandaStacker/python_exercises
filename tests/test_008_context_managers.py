from __future__ import annotations

import unittest

from tests.support import load_exercise


class FakeResource:
    def __init__(self) -> None:
        self.closed = False

    def close(self) -> None:
        self.closed = True


class ContextManagerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_exercise("008_context_managers.py")

    def test_closing_returns_resource_and_closes_normally(self) -> None:
        resource = FakeResource()
        with self.module.closing(resource) as entered:
            self.assertIs(entered, resource)
            self.assertFalse(resource.closed)
        self.assertTrue(resource.closed)

    def test_closing_does_not_suppress(self) -> None:
        resource = FakeResource()
        with self.assertRaisesRegex(RuntimeError, "boom"):
            with self.module.closing(resource):
                raise RuntimeError("boom")
        self.assertTrue(resource.closed)

    def test_temporary_value_restores_present_and_missing_keys(self) -> None:
        settings = {"mode": "normal"}
        with self.module.temporary_value(settings, "mode", "debug") as result:
            self.assertIs(result, settings)
            self.assertEqual(settings["mode"], "debug")
        self.assertEqual(settings, {"mode": "normal"})

        with self.assertRaises(KeyError):
            with self.module.temporary_value(settings, "extra", "yes"):
                self.assertEqual(settings["extra"], "yes")
                raise KeyError("leave")
        self.assertEqual(settings, {"mode": "normal"})

    def test_rollback_only_on_error(self) -> None:
        values = [1, 2]
        with self.module.rollback_on_error(values):
            values.extend([3, 4])
        self.assertEqual(values, [1, 2, 3, 4])

        identity = id(values)
        with self.assertRaisesRegex(ValueError, "invalid"):
            with self.module.rollback_on_error(values):
                values[:] = [99]
                raise ValueError("invalid")
        self.assertEqual(values, [1, 2, 3, 4])
        self.assertEqual(id(values), identity, "restore the same list instead of rebinding it")


if __name__ == "__main__":
    unittest.main()

