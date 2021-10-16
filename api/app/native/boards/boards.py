from aiohttp import web

from internal.container import DI_DATABASE_CLIENT, DI_LOGGER
from internal.database.errors import ErrorDatabase
from app.constants import APP_CONTAINER
from app.native.boards import (
    MessageBoard,
    MessageBoards,
    MessageGetBoard,
    MessageCreateBoard,
    MessageCreatedBoard,
    MessageUpdateBoard,
    MessageRemoveBoard,
    ErrorBoardIdNotFound,
    ErrorTitleAlreadyExists,
    ErrorNotFieldsToChange,
)


async def get_board(app: web.Application, msg: MessageGetBoard) -> MessageBoard:
    container = app[APP_CONTAINER]
    client = container.resolve(DI_DATABASE_CLIENT)
    logger = container.resolve(DI_LOGGER)

    query = "select * from boards.get(%(board_id)s)"
    params = {"board_id": msg.board_id}

    try:
        result = await client.fetchone(query, params)
    except Exception as err:
        logger.error(f"Failing to database: {type(err)}, {err}")
        raise ErrorDatabase

    error = result.get("error")
    if error is not None:
        logger.error(f"Failing to get board: {error}")
        if error["reason"] == "not_found" and error["description"] == "_board_id":
            raise ErrorBoardIdNotFound
        raise ErrorDatabase

    return MessageBoard(
        board_id=msg.board_id,
        title=result.get("title"),
        creator_id=result.get("creator_id"),
        created_at=result.get("created_at"),
    )


async def get_boards(app: web.Application) -> MessageBoards:
    container = app[APP_CONTAINER]
    client = container.resolve(DI_DATABASE_CLIENT)
    logger = container.resolve(DI_LOGGER)

    query = "select * from boards.search()"

    try:
        records = await client.fetchall(query)
    except Exception as err:
        logger.error(f"Failing to database: {type(err)}, {err}")
        raise ErrorDatabase

    message = MessageBoards(
        count=len(records),
        boards=[],
    )

    if not len(records):
        return message

    error = records[0].get("error")
    if error is not None:
        logger.error(f"Failing to get boards: {error}")

        raise ErrorDatabase

    for raw in records:
        item = MessageBoard(
            board_id=raw.get("board_id"),
            title=raw.get("title"),
            creator_id=raw.get("creator_id"),
            created_at=raw.get("created_at"),
        )
        message.boards.append(item)

    return message


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
        "creator_id": msg.creator_id,
    }
    try:
        result = await client.fetchone(query, params)
    except Exception as err:
        logger.error(f"Failing to database: {type(err)}, {err}")
        raise ErrorDatabase

    error = result.get("error")
    if error is not None:
        logger.error(f"Failing to create board: {error}")
        if error["reason"] == "exists" and error["description"] == "_title":
            raise ErrorTitleAlreadyExists
        if error["reason"] == "not_found" and error["description"] == "_creator_id":
            raise ErrorDatabase  # todo
        raise ErrorDatabase

    message = MessageCreatedBoard(
        board_id=result.get("board_id"),
        created_at=result.get("created_at"),
    )

    logger.info(f"Board {message.board_id} created.")

    return message


async def update_board(app: web.Application, msg: MessageUpdateBoard) -> None:
    container = app[APP_CONTAINER]
    client = container.resolve(DI_DATABASE_CLIENT)
    logger = container.resolve(DI_LOGGER)

    query = """
        select *
        from boards.update(
            %(board_id)s,
            %(title)s
        )
    """
    params = {
        "board_id": msg.board_id,
        "title": msg.title,
    }

    try:
        result = await client.fetchone(query, params)
    except Exception as err:
        logger.error(f"Failing to database: {type(err)}, {err}")
        raise ErrorDatabase

    error = result.get("error")
    if error is not None:
        logger.error(f"Failing to update board: {error}")
        if error["reason"] == "not_found" and error["description"] == "fields":
            raise ErrorNotFieldsToChange
        if error["reason"] == "not_found" and error["description"] == "_board_id":
            raise ErrorBoardIdNotFound

        raise ErrorDatabase

    logger.info(f"Board {msg.board_id} updated.")

    return None


async def remove_board(app: web.Application, msg: MessageRemoveBoard) -> None:
    container = app[APP_CONTAINER]
    client = container.resolve(DI_DATABASE_CLIENT)
    logger = container.resolve(DI_LOGGER)

    query = """
        select *
        from boards.delete(
            %(board_id)s
        )
    """
    params = {
        "board_id": msg.board_id,
    }

    try:
        result = await client.fetchone(query, params)
    except Exception as err:
        logger.error(f"Failing to database: {type(err)}, {err}")
        raise ErrorDatabase

    error = result.get("error")
    if error is not None:
        logger.error(f"Failing to remove board: {error}")
        if error["reason"] == "not_found" and error["description"] == "_board_id":
            raise ErrorBoardIdNotFound

        raise ErrorDatabase

    logger.info(f"Board {msg.board_id} deleted.")

    return None


