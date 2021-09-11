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

    client.connect()
    message = MessageCreatedUser(
        id="",
        created_at="",
    )

    return message
