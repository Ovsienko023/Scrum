from aiohttp.test_utils import unittest_run_loop

from tests.app.native.statuses import ScrumNativeStatusesTestCase
from app.native.statuses import MessageStatuses, MessageStatus


class ScrumNativeMessageStatusesTestCase(ScrumNativeStatusesTestCase):
    async def setUpAsync(self) -> None:
        self.message = MessageStatuses(
            count=1,
            statuses=[MessageStatus(title="new")]
        )

    @unittest_run_loop
    async def test_count(self):
        self.assertIsInstance(self.message.count, int)
        self.assertEqual(self.message.count, 1)

    @unittest_run_loop
    async def test_statuses(self):
        self.assertIsInstance(self.message.statuses, list)
        self.assertIsInstance(self.message.statuses[0], MessageStatus)

    @unittest_run_loop
    async def test_status_title(self):
        self.assertIsInstance(self.message.statuses[0].title, str)
        self.assertEqual(self.message.statuses[0].title, "new")


class ScrumNativeMessageStatusTestCase(ScrumNativeStatusesTestCase):
    async def setUpAsync(self) -> None:
        self.message = MessageStatus(title="new")

    @unittest_run_loop
    async def test_title(self):
        self.assertIsInstance(self.message.title, str)
        self.assertEqual(self.message.title, "new")
