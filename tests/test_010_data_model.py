from __future__ import annotations

from collections.abc import MutableSequence
import unittest

from tests.support import load_exercise


class DataModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_exercise("010_data_model.py")
        cls.Playlist = cls.module.Playlist

    def test_construction_iteration_indexing_and_repr(self) -> None:
        playlist = self.Playlist([" One ", "Two", " Three"])
        self.assertIsInstance(playlist, MutableSequence)
        self.assertEqual(len(playlist), 3)
        self.assertEqual(list(playlist), ["One", "Two", "Three"])
        self.assertEqual(playlist[-1], "Three")
        self.assertEqual(repr(playlist), "Playlist(['One', 'Two', 'Three'])")

    def test_slice_is_an_independent_playlist(self) -> None:
        original = self.Playlist(["a", "b", "c"])
        chosen = original[1:]
        self.assertIsInstance(chosen, self.Playlist)
        chosen.append("d")
        self.assertEqual(original, self.Playlist(["a", "b", "c"]))
        self.assertEqual(chosen, self.Playlist(["b", "c", "d"]))

    def test_mutable_sequence_operations_and_slice_assignment(self) -> None:
        playlist = self.Playlist(["a", "b"])
        playlist.append(" c ")
        playlist.insert(1, "new")
        playlist[0] = " first "
        playlist[1:3] = ["x", " y "]
        self.assertEqual(list(playlist), ["first", "x", "y", "c"])
        self.assertEqual(playlist.pop(), "c")
        del playlist[:2]
        self.assertEqual(list(playlist), ["y"])

    def test_every_mutation_validates(self) -> None:
        for operation in (
            lambda p: p.append(" "),
            lambda p: p.insert(0, 42),
            lambda p: p.__setitem__(0, ""),
            lambda p: p.__setitem__(slice(None), ["ok", " "]),
        ):
            playlist = self.Playlist(["original"])
            with self.subTest(operation=operation), self.assertRaises((TypeError, ValueError)):
                operation(playlist)
            self.assertEqual(playlist, self.Playlist(["original"]))

    def test_unrelated_equality(self) -> None:
        playlist = self.Playlist(["a"])
        self.assertFalse(playlist == ["a"])
        self.assertNotEqual(playlist, object())


if __name__ == "__main__":
    unittest.main()

