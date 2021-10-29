from aiohttp.test_utils import unittest_run_loop, make_mocked_coro

from app.native.statuses import MessageStatuses, MessageStatus
from app.native.statuses.statuses import get_statuses
from app.constants import APP_CONTAINER
from internal.container import DI_DATABASE_CLIENT
from tests.app.native.statuses import ScrumNativeStatusesTestCase


class ScrumNativeGetStatusesTestCase(ScrumNativeStatusesTestCase):
    @unittest_run_loop
    async def test_should_return_message(self):
        container = self.app[APP_CONTAINER]
        client = container.resolve(DI_DATABASE_CLIENT)
        client.fetchall = make_mocked_coro([{
            "error": None,
            "title": "new",
        }])

        result = await get_statuses(app=self.app)

        self.assertIsInstance(result, MessageStatuses)

    @unittest_run_loop
    async def test_should_have_count(self):
        container = self.app[APP_CONTAINER]
        client = container.resolve(DI_DATABASE_CLIENT)
        client.fetchall = make_mocked_coro([{
            "error": None,
            "title": "new",
        }])

        result = await get_statuses(app=self.app)

        self.assertIsInstance(result.count, int)
        self.assertEqual(result.count, 1)

    @unittest_run_loop
    async def test_should_have_statuses(self):
        container = self.app[APP_CONTAINER]
        client = container.resolve(DI_DATABASE_CLIENT)
        client.fetchall = make_mocked_coro([{
            "error": None,
            "title": "new",
        }])

        result = await get_statuses(app=self.app)

        self.assertIsInstance(result.statuses, list)

    @unittest_run_loop
    async def test_should_have_statuse(self):
        container = self.app[APP_CONTAINER]
        client = container.resolve(DI_DATABASE_CLIENT)
        client.fetchall = make_mocked_coro([{
            "error": None,
            "title": "new",
        }])

        result = await get_statuses(app=self.app)

        self.assertIsInstance(result.statuses[0], MessageStatus)

    @unittest_run_loop
    async def test_should_have_status_title(self):
        container = self.app[APP_CONTAINER]
        client = container.resolve(DI_DATABASE_CLIENT)
        client.fetchall = make_mocked_coro([{
            "error": None,
            "title": "new",
        }])

        result = await get_statuses(app=self.app)

        self.assertIsInstance(result.statuses[0].title, str)
        self.assertEqual(result.statuses[0].title, "new")
