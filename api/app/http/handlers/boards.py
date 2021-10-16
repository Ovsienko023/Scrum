from aiohttp import web
from marshmallow import ValidationError

from internal.database.errors import ErrorDatabase
from internal.container.constants import DI_LOGGER
from app.constants import APP_CONTAINER
from app.http.constants import ERROR_BAD_REQUEST, ERROR_UNKNOWN, ERROR_DATABASE
from app.http.schemas.boards import SchemaCreateBoard, SchemaGetBoard, SchemaUpdateBoard, SchemaRemoveBoard
from app.http.errors import ErrorContainer
from app.native.boards import (
    boards,
    MessageGetBoard,
    MessageCreateBoard,
    MessageUpdateBoard,
    MessageRemoveBoard,
    ErrorBoardIdNotFound,
    ErrorTitleAlreadyExists,
    ErrorNotFieldsToChange,
    ERROR_BOARD_ID_NOT_FOUND,
    ERROR_TITLE_ALREADY_EXISTS,
    ERROR_NOT_FIELDS_TO_CHANGE,

)


async def get_board(request) -> web.Response:
    errors = ErrorContainer()
    container = request.app[APP_CONTAINER]
    logger = container.resolve(DI_LOGGER)

    data = dict(request.match_info)
    schema = SchemaGetBoard()

    try:
        message = MessageGetBoard(**schema.load(data))
    except ValidationError as err:
        logger.error("Failed to get board. Validation error.")
        for field, error in err.messages.items():
            logger.error(f"Invalid field '{field}'. {error}")
            errors.add(f"invalid.{field}", error)

        return errors.done(400, ERROR_BAD_REQUEST)

    try:
        result = await boards.get_board(app=request.app, msg=message)
    except ErrorBoardIdNotFound:
        return errors.done(404, ERROR_BOARD_ID_NOT_FOUND)
    except ErrorDatabase:
        return errors.done(500, ERROR_DATABASE)
    except Exception as err:
        logger.error(f"Failed to get board. {type(err)}: {err}")
        return errors.done(500, ERROR_UNKNOWN)

    return web.json_response({
            "title": result.title,
            "creator_id": str(result.creator_id),
            "created_at": round(result.created_at.timestamp())
    })


async def get_boards(request) -> web.Response:
    errors = ErrorContainer()
    container = request.app[APP_CONTAINER]
    logger = container.resolve(DI_LOGGER)

    try:
        result = await boards.get_boards(app=request.app)
    except ErrorDatabase:
        return errors.done(500, ERROR_DATABASE)
    except Exception as err:
        logger.error(f"Failed to get boards. {type(err)}: {err}")
        return errors.done(500, ERROR_UNKNOWN)

    return web.json_response({
        "count": result.count,
        "boards": [
            {
                "id": str(board.board_id),
                "title": board.title,
                "creator_id": str(board.creator_id),
                "created_at": round(board.created_at.timestamp())
            }
            for board in result.boards
        ]
    })


async def create_board(request) -> web.Response:
    errors = ErrorContainer()
    container = request.app[APP_CONTAINER]
    logger = container.resolve(DI_LOGGER)

    try:
        data = await request.json()
    except ValueError as err:
        logger.error(f"Failed to create board.  ValueError: {err}")
        return errors.done(400, ERROR_BAD_REQUEST)

    schema = SchemaCreateBoard()

    try:
        message = MessageCreateBoard(**schema.load(data))
    except ValidationError as err:
        logger.error("Failed to create board. Validation error.")
        for field, error in err.messages.items():
            logger.error(f"Invalid field '{field}'. {error}")
            errors.add(f"invalid.{field}", error)

        return errors.done(400, ERROR_BAD_REQUEST)

    try:
        result = await boards.create_board(app=request.app, msg=message)
    except ErrorTitleAlreadyExists:
        return errors.done(404, ERROR_TITLE_ALREADY_EXISTS)
    except ErrorDatabase:
        return errors.done(500, ERROR_DATABASE)
    except Exception as err:
        logger.error(f"Failed to create board. {type(err)}: {err}")
        return errors.done(500, ERROR_UNKNOWN)

    return web.json_response({
         "id": str(result.board_id),
         "created_at": round(result.created_at.timestamp())
        })


async def update_board(request) -> web.Response:
    errors = ErrorContainer()
    container = request.app[APP_CONTAINER]
    logger = container.resolve(DI_LOGGER)

    try:
        data = await request.json()
        data["board_id"] = request.match_info["board_id"]
    except (ValueError, KeyError) as err:
        logger.error(f"Failed to update board.  ValueError: {err}")
        return errors.done(400, ERROR_BAD_REQUEST)

    schema = SchemaUpdateBoard()

    try:
        message = MessageUpdateBoard(**schema.load(data))
    except ValidationError as err:
        logger.error("Failed to update board. Validation error.")
        for field, error in err.messages.items():
            logger.error(f"Invalid field '{field}'. {error}")
            errors.add(f"invalid.{field}", error)

        return errors.done(400, ERROR_BAD_REQUEST)

    try:
        await boards.update_board(app=request.app, msg=message)
    except ErrorNotFieldsToChange:
        return errors.done(400, ERROR_NOT_FIELDS_TO_CHANGE)
    except ErrorBoardIdNotFound:
        return errors.done(404, ERROR_BOARD_ID_NOT_FOUND)
    except ErrorDatabase:
        return errors.done(500, ERROR_DATABASE)
    except Exception as err:
        logger.error(f"Failed to update board. {type(err)}: {err}")
        return errors.done(500, ERROR_UNKNOWN)

    return web.json_response()


async def remove_board(request) -> web.Response:
    errors = ErrorContainer()
    container = request.app[APP_CONTAINER]
    logger = container.resolve(DI_LOGGER)

    data = {"board_id":  request.match_info.get("board_id")}

    schema = SchemaRemoveBoard()

    try:
        message = MessageRemoveBoard(**schema.load(data))
    except ValidationError as err:
        logger.error("Failed to remove board. Validation error.")
        for field, error in err.messages.items():
            logger.error(f"Invalid field '{field}'. {error}")
            errors.add(f"invalid.{field}", error)

        return errors.done(400, ERROR_BAD_REQUEST)

    try:
        await boards.remove_board(app=request.app, msg=message)
    except ErrorBoardIdNotFound:
        return errors.done(404, ERROR_BOARD_ID_NOT_FOUND)
    except ErrorDatabase:
        return errors.done(500, ERROR_DATABASE)
    except Exception as err:
        logger.error(f"Failed to remove board. {type(err)}: {err}")
        return errors.done(500, ERROR_UNKNOWN)

    return web.json_response()
