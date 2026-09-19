from __future__ import annotations

import unittest

from tests.support import load_exercise


class PatternMatchingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_exercise("013_pattern_matching.py")

    def test_parse_each_command_shape(self) -> None:
        m = self.module
        self.assertEqual(m.parse_command(" MOVE North 3 "), m.Move(m.Direction.NORTH, 3))
        self.assertEqual(m.parse_command("say   Hello brave world"), m.Say("Hello brave world"))
        self.assertEqual(m.parse_command(" QuIt "), m.Quit())

    def test_invalid_commands_have_uniform_error(self) -> None:
        for text in ("", "move north", "move upward 2", "move west 0", "move east many", "say", "quit now"):
            with self.subTest(text=text), self.assertRaisesRegex(
                ValueError, f"^invalid command: {text}$"
            ):
                self.module.parse_command(text)

    def test_execute_transitions(self) -> None:
        m = self.module
        position, message = m.execute((10, 5), m.Move(m.Direction.WEST, 4))
        self.assertEqual(position, (6, 5))
        self.assertIsNone(message)
        self.assertEqual(m.execute(position, m.Say("hello")), (position, "hello"))
        self.assertEqual(m.execute(position, m.Quit()), (position, "quit"))

    def test_direction_vectors(self) -> None:
        m = self.module
        self.assertEqual(
            {direction.value: direction.vector for direction in m.Direction},
            {"north": (0, 1), "east": (1, 0), "south": (0, -1), "west": (-1, 0)},
        )


if __name__ == "__main__":
    unittest.main()

