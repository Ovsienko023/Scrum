import copy
from unittest.mock import MagicMock

from internal.logger.logger import get_logger
from internal.database.client import ClientDB
from internal.container.container import container
from internal.container.constants import (
    DI_CONFIG,
    DI_LOGGER,
    DI_DATABASE_CLIENT,
)


def mocked_config():
    config = container.resolve(DI_CONFIG)
    config["docs"]["enable"] = False
    return copy.copy(config)


mocked_client = MagicMock(ClientDB)
mocked_logger = MagicMock(get_logger())


container.register(DI_CONFIG, instance=mocked_config())
container.register(DI_LOGGER, instance=mocked_logger)
container.register(DI_DATABASE_CLIENT, instance=mocked_client)

mocked_container = container
