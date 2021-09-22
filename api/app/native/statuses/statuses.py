from aiohttp import web

from internal.container import DI_DATABASE_CLIENT, DI_LOGGER
from internal.database.errors import ErrorDatabase
from app.constants import APP_CONTAINER
from app.native.statuses import (
    MessageStatus,
    MessageStatuses,
)


async def get_statuses(app: web.Application) -> MessageStatuses:
    container = app[APP_CONTAINER]
    client = container.resolve(DI_DATABASE_CLIENT)
    logger = container.resolve(DI_LOGGER)

    query = "select * from statuses.search()"

    try:
        records = await client.fetchall(query)
    except Exception as err:
        logger.error(f"Failing to database: {type(err)}, {err}")
        raise ErrorDatabase

    message = MessageStatuses(
        count=len(records),
        statuses=[],
    )

    if not len(records):
        return message

    error = records[0].get("error")
    if error is not None:
        logger.error(f"Failing to get statuses: {error}")

        raise ErrorDatabase

    for raw in records:
        item = MessageStatus(
            status_id=raw.get("status_id"),
            title=raw.get("title"),
        )
        message.statuses.append(item)

    return message
