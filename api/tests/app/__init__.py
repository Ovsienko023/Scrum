import os
import warnings

from app.main import init_app
from tests import ScrumTestCase

from app.http.constants import REQUEST_USER_ID, APP_DISABLE_AUTHORIZATION


class ScrumAppTestCase(ScrumTestCase):
    async def get_application(self):
        warnings.filterwarnings("ignore")
        os.environ[APP_DISABLE_AUTHORIZATION] = "1"

        app = await init_app(self.container)

        return app
