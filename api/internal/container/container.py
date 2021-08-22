import punq

from internal.config.config import get_config
from internal.logger.logger import get_logger
from internal.container.constants import (
    DI_CONFIG,
    DI_LOGGER,
)


container = punq.Container()

container.register("DI_CONFIG", instance=get_config())
config = container.resolve("DI_CONFIG")

logger = get_logger()
logger.add(config["dirs"]["logger"], rotation="5MB", retention=5)
container.register("DI_LOGGER", instance=logger)



# instance_client = Manager(
#     host=config['db']['host'],
#     port=config['db']['port'],
#
# )
# container.register("DI_DATABASE_CLIENT", Manager, host=config['db']['host'], port=config['db']['port'])
