from aiohttp.test_utils import AioHTTPTestCase

from tests.utils.mocked import mocked_container


class ScrumTestCase(AioHTTPTestCase):
    def setUp(self) -> None:
        self.container = mocked_container
        super().setUp()
