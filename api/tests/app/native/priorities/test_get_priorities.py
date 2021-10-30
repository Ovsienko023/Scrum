from aiohttp.test_utils import unittest_run_loop, make_mocked_coro

from app.native.priorities import MessagePriorities, MessagePriority
from app.native.priorities.priorities import get_priorities
from app.constants import APP_CONTAINER
from internal.container import DI_DATABASE_CLIENT
from tests.app.native.priorities import ScrumNativePrioritiesTestCase


class ScrumNativeGetPrioritiesTestCase(ScrumNativePrioritiesTestCase):
    @unittest_run_loop
    async def test_should_return_message(self):
        container = self.app[APP_CONTAINER]
        client = container.resolve(DI_DATABASE_CLIENT)
        client.fetchall = make_mocked_coro([{
            "error": None,
            "title": "low",
        }])

        result = await get_priorities(app=self.app)

        self.assertIsInstance(result, MessagePriorities)

    @unittest_run_loop
    async def test_should_have_count(self):
        container = self.app[APP_CONTAINER]
        client = container.resolve(DI_DATABASE_CLIENT)
        client.fetchall = make_mocked_coro([{
            "error": None,
            "title": "low",
        }])

        result = await get_priorities(app=self.app)

        self.assertIsInstance(result.count, int)
        self.assertEqual(result.count, 1)

    @unittest_run_loop
    async def test_should_have_statuses(self):
        container = self.app[APP_CONTAINER]
        client = container.resolve(DI_DATABASE_CLIENT)
        client.fetchall = make_mocked_coro([{
            "error": None,
            "title": "low",
        }])

        result = await get_priorities(app=self.app)

        self.assertIsInstance(result.priorities, list)

    @unittest_run_loop
    async def test_should_have_priority(self):
        container = self.app[APP_CONTAINER]
        client = container.resolve(DI_DATABASE_CLIENT)
        client.fetchall = make_mocked_coro([{
            "error": None,
            "title": "low",
        }])

        result = await get_priorities(app=self.app)

        self.assertIsInstance(result.priorities[0], MessagePriority)

    @unittest_run_loop
    async def test_should_have_priority_title(self):
        container = self.app[APP_CONTAINER]
        client = container.resolve(DI_DATABASE_CLIENT)
        client.fetchall = make_mocked_coro([{
            "error": None,
            "title": "low",
        }])

        result = await get_priorities(app=self.app)

        self.assertIsInstance(result.priorities[0].title, str)
        self.assertEqual(result.priorities[0].title, "low")
