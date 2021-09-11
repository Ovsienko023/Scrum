import punq

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
logger.add(config["dirs"]["logger"], rotation="5MB", retention=5)
container.register(DI_LOGGER, instance=logger)

instance_client = ClientDB(
    database=config['db']['dbname'],  # "mcu",
    user=config['db']['user'],  # "postgres",
    password=config['db']['password'],  # "",
    host=config['db']['host'],
    port=config['db']['port'],
)
container.register(DI_DATABASE_CLIENT, instance=instance_client)


# client = ClientDB(dbname="mcu",
#                   user="postgres",
#                   password="",
#                   host="localhost",
#                   port=5432)
# client._connect()
# client.query("Select * from hub.users")
# print(client.fetchone())
# container.register("DI_DATABASE_CLIENT", ClientDB, host=config['db']['host'], port=config['db']['port'])