from __future__ import annotations

from dataclasses import dataclass
import unittest

from tests.support import load_exercise


@dataclass
class Note:
    id: str
    text: str


class MinimalReader:
    def __init__(self, notes):
        self.notes = notes

    def get(self, item_id):
        return next((note for note in self.notes if note.id == item_id), None)

    def __iter__(self):
        return iter(self.notes)


class ProtocolTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_exercise("014_typing_protocols.py")

    def test_repository_crud_and_order(self) -> None:
        repo = self.module.InMemoryRepository([Note("a", "first"), Note("b", "second")])
        self.assertEqual([note.id for note in repo], ["a", "b"])
        self.assertEqual(repo.get("b").text, "second")
        self.assertIsNone(repo.get("missing"))
        removed = repo.remove("a")
        self.assertEqual(removed.id, "a")
        with self.assertRaises(KeyError):
            repo.remove("absent")

    def test_repository_validates_protocol_and_duplicates(self) -> None:
        repo = self.module.InMemoryRepository()
        with self.assertRaises(TypeError):
            repo.add(object())
        repo.add(Note("same", "one"))
        with self.assertRaisesRegex(ValueError, "^duplicate id: same$"):
            repo.add(Note("same", "two"))

    def test_functions_accept_a_structural_reader(self) -> None:
        notes = [Note("a", "ordinary"), Note("b", "important"), Note("c", "important too")]
        source = MinimalReader(notes)
        self.assertEqual(self.module.find_first(source, lambda note: "important" in note.text), notes[1])
        self.assertIsNone(self.module.find_first(source, lambda note: note.id == "z"))

        destination = self.module.InMemoryRepository()
        count = self.module.copy_matching(source, destination, lambda note: note.text.startswith("important"))
        self.assertEqual(count, 2)
        self.assertEqual(list(destination), notes[1:])

    def test_identified_protocol_is_runtime_checkable(self) -> None:
        self.assertIsInstance(Note("x", "text"), self.module.Identified)
        self.assertNotIsInstance(object(), self.module.Identified)


if __name__ == "__main__":
    unittest.main()

