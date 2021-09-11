from aiohttp import web

from internal.container import DI_DATABASE_CLIENT
from app.constants import APP_CONTAINER
from app.native.users import (
    MessageCreateUser,
    MessageCreatedUser,
)


async def create_user(app: web.Application, msg: MessageCreateUser) -> MessageCreatedUser:
    container = app[APP_CONTAINER]
    client = container.resolve(DI_DATABASE_CLIENT)

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

    result = await client.fetchone(query, params)

    message = MessageCreatedUser(
        user_id=result.get("user_id"),
        created_at=result.get("created_at"),
    )

    return message
