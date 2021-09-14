from aiohttp import web

from internal.container import DI_DATABASE_CLIENT, DI_LOGGER
from internal.database.errors import ErrorDatabase
from app.constants import APP_CONTAINER
from app.native.cards import (
    MessageCreateCard,
    MessageCreatedCard,
)


async def create_card(app: web.Application, msg: MessageCreateCard) -> MessageCreatedCard:
    container = app[APP_CONTAINER]
    client = container.resolve(DI_DATABASE_CLIENT)
    logger = container.resolve(DI_LOGGER)

    query = """
        select *
        from cards.create(
            %(title)s,
            %(description)s,
            %(developer_id)s,
            %(priority_id)s,
            %(status_id)s,
            %(board_id)s,
            %(creator_id)s,
            %(estimates_time)s
        )
    """
    params = {
        "title": msg.title,
        "description": msg.description,
        "developer_id": msg.developer_id,
        "priority_id": msg.priority_id,
        "status_id": msg.status_id,
        "board_id": msg.board_id,
        "creator_id": "a24d94d1-2340-4ca2-b765-2384a7a33191",  # todo add oauth
        "estimates_time": msg.estimates_time,
    }

    try:
        result = await client.fetchone(query, params)
    except Exception as err:
        logger.error(f"Failing to database: {type(err)}, {err}")
        raise ErrorDatabase

    message = MessageCreatedCard(
        card_id=result.get("board_id"),
        created_at=result.get("created_at"),
    )

    logger.info(f"Card {message.card_id} created.")

    return message
