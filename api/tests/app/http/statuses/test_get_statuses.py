from aiohttp.test_utils import unittest_run_loop
from unittest.mock import MagicMock, patch

from tests.app.http.statuses import HTTPStatusesTestCase
from app.native.statuses import MessageStatuses, MessageStatus


class TestHTTPGetStatuses(HTTPStatusesTestCase):
    MOCKED_GET_STATUSES = "app.native.statuses.statuses.get_statuses"
    URL_GET_STATUSES = "/misc/statuses"

    @unittest_run_loop
    async def test_response_is_dict(self):
        message = MagicMock(
            spec=MessageStatuses,
            count=1,
            statuses=[MagicMock(spec=MessageStatus, title="new")]
        )

        with patch(self.MOCKED_GET_STATUSES, return_value=message):
            resp = await self.client.request("GET", self.URL_GET_STATUSES)
            body = await resp.json()

            self.assertIsInstance(body, dict)

    @unittest_run_loop
    async def test_response_count(self):
        message = MagicMock(
            spec=MessageStatuses,
            count=1,
            statuses=[MagicMock(spec=MessageStatus, title="new")]
        )

        with patch(self.MOCKED_GET_STATUSES, return_value=message):
            resp = await self.client.request("GET", self.URL_GET_STATUSES)
            body = await resp.json()

            self.assertIsInstance(body["count"], int)
            self.assertEqual(body["count"], 1)

    @unittest_run_loop
    async def test_response_statuses_is_list(self):
        message = MagicMock(
            spec=MessageStatuses,
            count=1,
            statuses=[MagicMock(spec=MessageStatus, title="new")]
        )

        with patch(self.MOCKED_GET_STATUSES, return_value=message):
            resp = await self.client.request("GET", self.URL_GET_STATUSES)
            body = await resp.json()

            self.assertIsInstance(body["statuses"], list)

    @unittest_run_loop
    async def test_response_statuses(self):
        message = MagicMock(
            spec=MessageStatuses,
            count=1,
            statuses=[MagicMock(spec=MessageStatus, title="new")]
        )

        with patch(self.MOCKED_GET_STATUSES, return_value=message):
            resp = await self.client.request("GET", self.URL_GET_STATUSES)
            body = await resp.json()

            status = body["statuses"][0]

            self.assertIsInstance(status, str)
            self.assertEqual(status, "new")
            self.assertEqual(len(body["statuses"]), 1)
