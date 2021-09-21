from aiohttp import web

from internal.container import DI_DATABASE_CLIENT, DI_LOGGER
from internal.database.errors import ErrorDatabase
from app.constants import APP_CONTAINER
from app.native.estimation import EstimationTime
from app.native.cards import (
    MessageCard,
    MessageGetCard,
    MessageCreateCard,
    MessageCreatedCard,
    MessageUpdateCard,
    MessageGetReport,
    MessageReported,
    MessageRemoveCard,
    ErrorCardIdNotFound,
    ErrorBordNotFound,
    ErrorStatusNotFound,
    ErrorPriorityNotFound,
    ErrorDeveloperNotFound,
    ErrorNotFieldsToChange,
)


async def get_card(app: web.Application, msg: MessageGetCard) -> MessageCard:
    container = app[APP_CONTAINER]
    client = container.resolve(DI_DATABASE_CLIENT)
    logger = container.resolve(DI_LOGGER)

    query = "select * from cards.get(%(card_id)s)"
    params = {"card_id": msg.card_id}

    try:
        result = await client.fetchone(query, params)
    except Exception as err:
        logger.error(f"Failing to database: {type(err)}, {err}")
        raise ErrorDatabase

    error = result.get("error")
    if error is not None:
        logger.error(f"Failing to get card: {error}")
        if error["reason"] == "not_found" and error["description"] == "_card_id":
            raise ErrorCardIdNotFound
        raise ErrorDatabase

    return MessageCard(
        card_id=msg.card_id,
        title=result.get("title"),
        description=result.get("description"),
        developer_id=result.get("developer_id"),
        priority=result.get("priority"),
        status=result.get("status"),
        estimates_time=result.get("estimates_time"),
        board_id=result.get("board_id"),
        creator_id=result.get("creator_id"),
        created_at=result.get("created_at"),
        updated_at=result.get("updated_at"),
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
        "estimates_time": msg.estimation,
    }

    try:
        result = await client.fetchone(query, params)
    except Exception as err:
        logger.error(f"Failing to database: {type(err)}, {err}")
        raise ErrorDatabase

    error = result.get("error")
    if error is not None:
        logger.error(f"Failing to create cards: {error}")
        if error["reason"] == "not_found" and error["description"] == "_developer_id":
            raise ErrorDeveloperNotFound
        if error["reason"] == "not_found" and error["description"] == "_priority_id":
            raise ErrorPriorityNotFound
        if error["reason"] == "not_found" and error["description"] == "_status_id":
            raise ErrorStatusNotFound
        if error["reason"] == "not_found" and error["description"] == "_board_id":
            raise ErrorBordNotFound
        if error["reason"] == "not_found" and error["description"] == "_creator_id":
            raise ErrorDatabase
        raise ErrorDatabase

    message = MessageCreatedCard(
        card_id=result.get("card_id"),
        created_at=result.get("created_at"),
    )

    logger.info(f"Card {message.card_id} created.")

    return message


async def update_card(app: web.Application, msg: MessageUpdateCard) -> None:
    container = app[APP_CONTAINER]
    client = container.resolve(DI_DATABASE_CLIENT)
    logger = container.resolve(DI_LOGGER)

    query = """
        select *
        from cards.update(
            %(card_id)s,
            %(title)s,
            %(description)s,
            %(developer_id)s,
            %(priority_id)s,
            %(status_id)s,
            %(board_id)s,
            %(estimates_time)s
        )
    """
    params = {
        "card_id": msg.card_id,
        "title": msg.title,
        "description": msg.description,
        "developer_id": msg.developer_id,
        "priority_id": msg.priority_id,
        "status_id": msg.status_id,
        "board_id": msg.board_id,
        "estimates_time": msg.estimation,
    }

    try:
        result = await client.fetchone(query, params)
    except Exception as err:
        logger.error(f"Failing to database: {type(err)}, {err}")
        raise ErrorDatabase

    error = result.get("error")
    if error is not None:
        logger.error(f"Failing to update cards: {error}")
        if error["reason"] == "exists" and error["description"] == "_card_id":
            raise ErrorCardIdNotFound
        if error["reason"] == "not_found" and error["description"] == "_developer_id":
            raise ErrorDeveloperNotFound
        if error["reason"] == "not_found" and error["description"] == "_priority_id":
            raise ErrorPriorityNotFound
        if error["reason"] == "not_found" and error["description"] == "_status_id":
            raise ErrorStatusNotFound
        if error["reason"] == "not_found" and error["description"] == "_board_id":
            raise ErrorBordNotFound
        if error["reason"] == "not_found" and error["description"] == "_board_id":
            raise ErrorBordNotFound
        if error["reason"] == "not_found" and error["description"] == "fields":
            raise ErrorNotFieldsToChange

        raise ErrorDatabase

    logger.info(f"Card {msg.card_id} updated.")

    return None


async def get_report(app: web.Application, msg: MessageGetReport) -> MessageReported:
    container = app[APP_CONTAINER]
    client = container.resolve(DI_DATABASE_CLIENT)
    logger = container.resolve(DI_LOGGER)

    query = """
        select *
        from cards.report(
            %(board_id)s,
            %(status_id)s,
            %(priority_id)s,
            %(developer_id)s
        )
    """
    params = {
        "board_id": msg.board_id,
        "status_id": msg.status_id,
        "priority_id": msg.priority_id,
        "developer_id": msg.developer_id,
    }

    try:
        result = await client.fetchall(query, params)
    except Exception as err:
        logger.error(f"Failing to database: {type(err)}, {err}")
        raise ErrorDatabase

    error = result[0].get("error")

    if error is not None:
        logger.error(f"Failing to get report: {error}")

        if error["reason"] == "not_found" and error["description"] == "_board_id":
            raise ErrorBordNotFound
        if error["reason"] == "not_found" and error["description"] == "_status_id":
            raise ErrorStatusNotFound
        if error["reason"] == "not_found" and error["description"] == "_priority_id":
            raise ErrorPriorityNotFound
        if error["reason"] == "not_found" and error["description"] == "_developer_id":
            raise ErrorDeveloperNotFound

        raise ErrorDatabase

    message = MessageReported(
        estimation=EstimationTime(0),
        cards=[],
    )

    for card in result:
        message.estimation += EstimationTime(
            hours=card.get("estimates_time")
        )

        item = MessageCard(
            card_id=card.get("card_id"),
            title=card.get("title"),
            description=card.get("description"),
            developer_id=card.get("developer_id"),
            priority=card.get("priority"),
            status=card.get("status"),
            estimates_time=card.get("estimates_time"),
            board_id=card.get("board_id"),
            creator_id=card.get("creator_id"),
            created_at=card.get("created_at"),
            updated_at=card.get("updated_at"),
        )
        message.cards.append(item)

    return message


async def remove_card(app: web.Application, msg: MessageRemoveCard) -> None:
    container = app[APP_CONTAINER]
    client = container.resolve(DI_DATABASE_CLIENT)
    logger = container.resolve(DI_LOGGER)

    query = """
        select *
        from cards.delete(
            %(card_id)s
        )
    """
    params = {
        "card_id": msg.card_id,
    }

    try:
        result = await client.fetchone(query, params)
    except Exception as err:
        logger.error(f"Failing to database: {type(err)}, {err}")
        raise ErrorDatabase

    error = result.get("error")
    if error is not None:
        logger.error(f"Failing to remove card: {error}")
        if error["reason"] == "not_found" and error["description"] == "_card_id":
            raise ErrorCardIdNotFound

        raise ErrorDatabase

    logger.info(f"Card {msg.card_id} deleted.")

    return None
