from __future__ import annotations

import unittest

from tests.support import load_exercise


class CountingStore:
    def __init__(self):
        self.values = {}
        self.get_calls = 0
    def get(self, key):
        self.get_calls += 1
        return self.values[key]
    def set(self, key, value):
        self.values[key] = value
    def delete(self, key):
        del self.values[key]


class LayeredStoreTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_exercise("027_layered_stores.py")

    def test_memory_store_has_mapping_semantics_and_matches_protocol(self) -> None:
        store = self.module.MemoryStore()
        self.assertIsInstance(store, self.module.Store)
        with self.assertRaises(KeyError):
            store.get("missing")
        store.set("answer", 42)
        self.assertEqual(store.get("answer"), 42)
        store.delete("answer")
        with self.assertRaises(KeyError):
            store.delete("answer")

    def test_namespace_is_an_adapter_not_separate_storage(self) -> None:
        inner = self.module.MemoryStore()
        left = self.module.NamespacedStore(inner, " left ")
        right = self.module.NamespacedStore(inner, "right")
        left.set("color", "blue")
        right.set("color", "red")
        self.assertEqual(inner.get("left:color"), "blue")
        self.assertEqual(right.get("color"), "red")
        with self.assertRaises(ValueError):
            self.module.NamespacedStore(inner, " ")

    def test_json_store_translates_at_the_boundary(self) -> None:
        inner = self.module.MemoryStore()
        store = self.module.JsonStore(inner)
        value = {"b": [2, 3], "a": 1}
        store.set("document", value)
        self.assertEqual(inner.get("document"), '{"a": 1, "b": [2, 3]}')
        self.assertEqual(store.get("document"), value)
        store.delete("document")
        with self.assertRaises(KeyError):
            store.get("document")

    def test_cache_remembers_values_and_absence(self) -> None:
        inner = CountingStore()
        inner.set("x", 1)
        cache = self.module.CachedStore(inner)
        self.assertEqual(cache.get("x"), 1)
        self.assertEqual(cache.get("x"), 1)
        self.assertEqual(inner.get_calls, 1)
        for _ in range(2):
            with self.assertRaises(KeyError):
                cache.get("missing")
        self.assertEqual(inner.get_calls, 2, "missing keys should also be cached")
        self.assertIs(cache.cache["missing"], self.module.MISSING)
        cache.set("x", 2)
        self.assertEqual(cache.get("x"), 2)
        cache.delete("x")
        self.assertIs(cache.cache["x"], self.module.MISSING)

    def test_temporary_value_restores_value_or_absence_after_errors(self) -> None:
        store = self.module.MemoryStore()
        store.set("mode", None)
        with self.module.temporary_value(store, "mode", "debug") as entered:
            self.assertIs(entered, store)
            self.assertEqual(store.get("mode"), "debug")
        self.assertIsNone(store.get("mode"))
        with self.assertRaisesRegex(RuntimeError, "boom"):
            with self.module.temporary_value(store, "new", 3):
                raise RuntimeError("boom")
        with self.assertRaises(KeyError):
            store.get("new")

    def test_layers_compose_through_the_protocol(self) -> None:
        raw = self.module.MemoryStore()
        namespaced = self.module.NamespacedStore(raw, "settings")
        documents = self.module.JsonStore(namespaced)
        cached = self.module.CachedStore(documents)
        cached.set("theme", {"dark": True})
        self.assertEqual(cached.get("theme"), {"dark": True})
        self.assertEqual(raw.get("settings:theme"), '{"dark": true}')


if __name__ == "__main__":
    unittest.main()
