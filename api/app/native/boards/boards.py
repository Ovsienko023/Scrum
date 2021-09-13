from aiohttp import web

from internal.container import DI_DATABASE_CLIENT, DI_LOGGER
from internal.database.errors import ErrorDatabase
from app.constants import APP_CONTAINER
from app.native.boards import (
    MessageCreateBoard,
    MessageCreatedBoard,
)


async def create_board(app: web.Application, msg: MessageCreateBoard) -> MessageCreatedBoard:
    container = app[APP_CONTAINER]
    client = container.resolve(DI_DATABASE_CLIENT)
    logger = container.resolve(DI_LOGGER)

    query = """
        select *
        from boards.create(
            %(title)s,
            %(creator_id)s
        )
    """
    params = {
        "title": msg.title,
        "creator_id": "a24d94d1-2340-4ca2-b765-2384a7a33191",  # todo add oauth
    }
    try:
        result = await client.fetchone(query, params)
    except Exception as err:
        logger.error(f"Failing to database: {type(err)}, {err}")
        raise ErrorDatabase

    message = MessageCreatedBoard(
        board_id=result.get("board_id"),
        created_at=result.get("created_at"),
    )

    logger.info(f"Board {message.board_id} created.")

    return message
