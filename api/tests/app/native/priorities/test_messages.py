from aiohttp.test_utils import unittest_run_loop

from tests.app.native.priorities import ScrumNativePrioritiesTestCase
from app.native.priorities import MessagePriorities, MessagePriority


class ScrumNativeMessagePrioritiesTestCase(ScrumNativePrioritiesTestCase):
    async def setUpAsync(self) -> None:
        self.message = MessagePriorities(
            count=1,
            priorities=[MessagePriority(title="low")]
        )

    @unittest_run_loop
    async def test_count(self):
        self.assertIsInstance(self.message.count, int)
        self.assertEqual(self.message.count, 1)

    @unittest_run_loop
    async def test_statuses(self):
        self.assertIsInstance(self.message.priorities, list)
        self.assertIsInstance(self.message.priorities[0], MessagePriority)

    @unittest_run_loop
    async def test_status_title(self):
        self.assertIsInstance(self.message.priorities[0].title, str)
        self.assertEqual(self.message.priorities[0].title, "low")


class ScrumNativeMessagePriorityTestCase(ScrumNativePrioritiesTestCase):
    async def setUpAsync(self) -> None:
        self.message = MessagePriority(title="low")

    @unittest_run_loop
    async def test_title(self):
        self.assertIsInstance(self.message.title, str)
        self.assertEqual(self.message.title, "low")
