from aiohttp import web

from internal.database.errors import ErrorDatabase
from internal.container import DI_DATABASE_CLIENT, DI_LOGGER
from app.constants import APP_CONTAINER
from app.native.users import (
    MessageCreateUser,
    MessageCreatedUser,
)


async def create_user(app: web.Application, msg: MessageCreateUser) -> MessageCreatedUser:
    container = app[APP_CONTAINER]
    client = container.resolve(DI_DATABASE_CLIENT)
    logger = container.resolve(DI_LOGGER)

    query = """
        select *
        from users.create(
            %(name)s,
            %(hash)s
        )
    """
    params = {
        "name": msg.name,
        "hash": msg.password,
    }
    try:
        result = await client.fetchone(query, params)
    except Exception as err:
        logger.error(f"Failing to database: {type(err)}, {err}")
        raise ErrorDatabase

    message = MessageCreatedUser(
        user_id=result.get("user_id"),
        created_at=result.get("created_at"),
    )

    logger.info(f"User {message.user_id} created.")

    return message
