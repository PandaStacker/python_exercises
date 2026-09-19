from __future__ import annotations

import asyncio
import unittest

from tests.support import load_exercise


class AsyncOrchestrationTests(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_exercise("017_async_orchestration.py")

    async def test_bounded_map_limits_work_and_preserves_order(self) -> None:
        active = 0
        maximum = 0

        async def worker(value):
            nonlocal active, maximum
            active += 1
            maximum = max(maximum, active)
            try:
                await asyncio.sleep((5 - value) * 0.002)
                return value * 10
            finally:
                active -= 1

        result = await self.module.bounded_map(worker, range(6), limit=2)
        self.assertEqual(result, [0, 10, 20, 30, 40, 50])
        self.assertLessEqual(maximum, 2)
        self.assertGreater(maximum, 1)
        with self.assertRaises(ValueError):
            await self.module.bounded_map(worker, [], limit=0)

    async def test_bounded_map_cleans_up_siblings_on_failure(self) -> None:
        cancelled = asyncio.Event()

        async def worker(value):
            if value == "bad":
                await asyncio.sleep(0)
                raise LookupError("broken")
            try:
                await asyncio.sleep(10)
            except asyncio.CancelledError:
                cancelled.set()
                raise

        with self.assertRaisesRegex(LookupError, "broken"):
            await self.module.bounded_map(worker, ["slow", "bad", "later"], limit=2)
        self.assertTrue(cancelled.is_set())

    async def test_first_success_uses_completion_order_and_cleans_up(self) -> None:
        cancelled = asyncio.Event()

        async def fail():
            await asyncio.sleep(0.001)
            raise ValueError("early failure")

        async def win():
            await asyncio.sleep(0.002)
            return "winner"

        async def slow():
            try:
                await asyncio.sleep(10)
            except asyncio.CancelledError:
                cancelled.set()
                raise

        self.assertEqual(await self.module.first_success([slow(), fail(), win()]), "winner")
        self.assertTrue(cancelled.is_set())

    async def test_first_success_groups_failures_and_rejects_empty(self) -> None:
        async def fail(error):
            raise error

        with self.assertRaises(ExceptionGroup) as caught:
            await self.module.first_success([fail(ValueError("a")), fail(LookupError("b"))])
        self.assertEqual(caught.exception.message, "all operations failed")
        self.assertEqual(len(caught.exception.exceptions), 2)
        with self.assertRaisesRegex(ValueError, "at least one awaitable is required"):
            await self.module.first_success([])

    async def test_timeout_distinguishes_missing_from_none(self) -> None:
        cancelled = asyncio.Event()

        async def slow():
            try:
                await asyncio.sleep(10)
            except asyncio.CancelledError:
                cancelled.set()
                raise

        self.assertIsNone(await self.module.with_timeout(slow(), 0.001, fallback=None))
        self.assertTrue(cancelled.is_set())
        with self.assertRaises(TimeoutError):
            await self.module.with_timeout(asyncio.sleep(10), 0.001)
        self.assertEqual(await self.module.with_timeout(asyncio.sleep(0, result=42), 1), 42)


if __name__ == "__main__":
    unittest.main()

