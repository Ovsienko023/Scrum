from aiohttp import web
from hashlib import sha256

from internal.database.errors import ErrorDatabase
from internal.container import DI_DATABASE_CLIENT, DI_LOGGER
from app.constants import APP_CONTAINER
from app.native.users import (
    MessageCreateUser,
    MessageCreatedUser,
    ErrorLoginAlreadyExists,
)


async def create_user(app: web.Application, msg: MessageCreateUser) -> MessageCreatedUser:
    container = app[APP_CONTAINER]
    client = container.resolve(DI_DATABASE_CLIENT)
    logger = container.resolve(DI_LOGGER)

    password_hash = sha256(msg.password.encode("utf-8")).hexdigest()

    query = """
        select *
        from users.create(
            %(display_name)s,
            %(login)s,
            %(hash)s
        )
    """
    params = {
        "display_name": msg.display_name,
        "login": msg.login,
        "hash": password_hash,
    }
    try:
        result = await client.fetchone(query, params)
    except Exception as err:
        logger.error(f"Failing to database: {type(err)}, {err}")
        raise ErrorDatabase

    error = result.get("error")
    if error is not None:
        if error["reason"] == "exists" and error["description"] == "_login":
            raise ErrorLoginAlreadyExists

    message = MessageCreatedUser(
        user_id=result.get("user_id"),
        created_at=result.get("created_at"),
    )

    logger.info(f"User {message.user_id} created.")

    return message
