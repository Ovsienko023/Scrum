from aiohttp.test_utils import unittest_run_loop
from unittest.mock import MagicMock, patch

from tests.app.http.statuses import HTTPStatusesTestCase


class TestHTTPGetStatuses(HTTPStatusesTestCase):
    MOCKED_GET_STATUSES = ""
    URL_GET_STATUSES = "/misc/statuses"

    @unittest_run_loop
    async def test_native_called_once(self):
        # mock_message = MagicMock(
        #     spec=MessageLocales,
        #     count=1,
        #     locales=[{"id": "en_US", "description": "English"}]
        # )
        #
        # with patch("app.api.native.locales.locales.get_locales", return_value=mock_message) as mock_locale:
        resp = await self.client.request("GET", self.URL_GET_STATUSES)
        print(resp.status)
        print(resp)
