from aiohttp import web
from app.native.users import (
    MessageCreateUser,
    MessageCreatedUser,
)


async def create_user(app: web.Application, msg: MessageCreateUser) -> MessageCreatedUser:


    message = MessageCreatedUser(
        id="",
        created_at="",
    )

    return message
