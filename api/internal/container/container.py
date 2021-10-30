import punq
from pathlib import Path

from internal.config.config import get_config
from internal.logger.logger import get_logger
from internal.database.client import ClientDB
from internal.container.constants import (
    DI_CONFIG,
    DI_LOGGER,
    DI_DATABASE_CLIENT,
)


container = punq.Container()

container.register(DI_CONFIG, instance=get_config())
config = container.resolve(DI_CONFIG)

logger = get_logger()
logger.add(Path(config["dirs"]["logger"]), rotation="5MB", retention=5)
container.register(DI_LOGGER, instance=logger)

instance_client = ClientDB(
    database=Path(config["db"]["dbname"]),
    user=Path(config["db"]["user"]),
    password=Path(config["db"]["password"]),
    host=Path(config["db"]["host"]),
    port=Path(config["db"]["port"]),
)
container.register(DI_DATABASE_CLIENT, instance=instance_client)
