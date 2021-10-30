from aiohttp.test_utils import unittest_run_loop
from unittest.mock import MagicMock, patch

from tests.app.http.priorities import HTTPPrioritiesTestCase
from app.native.priorities import MessagePriorities, MessagePriority


class TestHTTPGetPriorities(HTTPPrioritiesTestCase):
    MOCKED_GET_PRIORITIES = "app.native.priorities.priorities.get_priorities"
    URL_GET_PRIORITIES = "/misc/priorities"

    @unittest_run_loop
    async def test_response_is_dict(self):
        message = MagicMock(
            spec=MessagePriorities,
            count=1,
            priorities=[MagicMock(spec=MessagePriority, title="low")]
        )

        with patch(self.MOCKED_GET_PRIORITIES, return_value=message):
            resp = await self.client.request("GET", self.URL_GET_PRIORITIES)
            body = await resp.json()

            self.assertIsInstance(body, dict)

    @unittest_run_loop
    async def test_response_count(self):
        message = MagicMock(
            spec=MessagePriorities,
            count=1,
            priorities=[MagicMock(spec=MessagePriority, title="low")]
        )

        with patch(self.MOCKED_GET_PRIORITIES, return_value=message):
            resp = await self.client.request("GET", self.URL_GET_PRIORITIES)
            body = await resp.json()

            self.assertIsInstance(body["count"], int)
            self.assertEqual(body["count"], 1)

    @unittest_run_loop
    async def test_response_statuses_is_list(self):
        message = MagicMock(
            spec=MessagePriorities,
            count=1,
            priorities=[MagicMock(spec=MessagePriority, title="low")]
        )

        with patch(self.MOCKED_GET_PRIORITIES, return_value=message):
            resp = await self.client.request("GET", self.URL_GET_PRIORITIES)
            body = await resp.json()

            self.assertIsInstance(body["priorities"], list)

    @unittest_run_loop
    async def test_response_priorities(self):
        message = MagicMock(
            spec=MessagePriorities,
            count=1,
            priorities=[MagicMock(spec=MessagePriority, title="low")]
        )

        with patch(self.MOCKED_GET_PRIORITIES, return_value=message):
            resp = await self.client.request("GET", self.URL_GET_PRIORITIES)
            body = await resp.json()

            status = body["priorities"][0]

            self.assertIsInstance(status, str)
            self.assertEqual(status, "low")
            self.assertEqual(len(body["priorities"]), 1)
