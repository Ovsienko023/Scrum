from aiohttp import web

from internal.container import DI_DATABASE_CLIENT, DI_LOGGER
from internal.database.errors import ErrorDatabase
from app.constants import APP_CONTAINER
from app.native.priorities import (
    MessagePriority,
    MessagePriorities,
)


async def get_priorities(app: web.Application) -> MessagePriorities:
    container = app[APP_CONTAINER]
    client = container.resolve(DI_DATABASE_CLIENT)
    logger = container.resolve(DI_LOGGER)

    query = "select * from priorities.search()"

    try:
        records = await client.fetchall(query)
    except Exception as err:
        logger.error(f"Failing to database: {type(err)}, {err}")
        raise ErrorDatabase

    message = MessagePriorities(
        count=len(records),
        priorities=[],
    )

    if not len(records):
        return message

    error = records[0].get("error")
    if error is not None:
        logger.error(f"Failing to get priorities: {error}")

        raise ErrorDatabase

    for raw in records:
        item = MessagePriority(
            priority_id=raw.get("priority_id"),
            title=raw.get("title"),
        )
        message.priorities.append(item)

    return message
