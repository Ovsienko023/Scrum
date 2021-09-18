from aiohttp import web
from marshmallow import ValidationError

from internal.database.errors import ErrorDatabase
from internal.container.constants import DI_LOGGER
from app.constants import APP_CONTAINER, ERROR_BAD_REQUEST, ERROR_UNKNOWN, ERROR_DATABASE
from app.http.schemas.cards import SchemaGetCard, SchemaCreateCard
from app.http.errors import ErrorContainer
from app.native.estimation import EstimationTime
from app.native.cards import (
    cards,
    MessageGetCard,
    MessageCreateCard,
    ErrorCardIdNotFound,
    ErrorTitleAlreadyExists,
    ErrorBordNotFound,
    ErrorStatusNotFound,
    ErrorPriorityNotFound,
    ErrorDeveloperNotFound,
    ERROR_TITLE_ALREADY_EXISTS,
    ERROR_BOARD_NOT_FOUND,
    ERROR_STATUS_NOT_FOUND,
    ERROR_PRIORITY_NOT_FOUND,
    ERROR_DEVELOPER_NOT_FOUND,
    ERROR_CARD_ID_NOT_FOUND,
)


async def get_card(request) -> web.Response:
    errors = ErrorContainer()
    container = request.app[APP_CONTAINER]
    logger = container.resolve(DI_LOGGER)

    data = dict(request.match_info)
    schema = SchemaGetCard()

    try:
        message = MessageGetCard(**schema.load(data))
    except ValidationError as err:
        logger.error("Failed to get card. Validation error.")
        for field, error in err.messages.items():
            logger.error(f"Invalid field '{field}'. {error}")
            errors.add(f"invalid.{field}", error)

    if not errors.is_empty():
        return errors.done(400, ERROR_BAD_REQUEST)

    try:
        result = await cards.get_card(app=request.app, msg=message)
    except ErrorCardIdNotFound:
        return errors.done(404, ERROR_CARD_ID_NOT_FOUND)
    except ErrorDatabase:
        return errors.done(500, ERROR_DATABASE)
    except Exception as err:
        logger.error(f"Failed to get card. {type(err)}: {err}")
        return errors.done(500, ERROR_UNKNOWN)

    return web.json_response({
            "title": result.title,
            "description": result.description,
            "developer_id": str(result.developer_id),
            "priority": result.priority,
            "status": result.status,
            "estimates_time": str(EstimationTime(hours=result.estimates_time)),
            "board_id": str(result.board_id),
            "creator_id": str(result.creator_id),
            "created_at": round(result.created_at.timestamp())
    })


async def create_card(request) -> web.Response:
    errors = ErrorContainer()
    container = request.app[APP_CONTAINER]
    logger = container.resolve(DI_LOGGER)

    try:
        data = await request.json()
    except ValueError as err:
        logger.error(f"Failed to create card.  ValueError: {err}")
        return errors.done(400, ERROR_BAD_REQUEST)

    schema = SchemaCreateCard()

    try:
        message = MessageCreateCard(**schema.load(data))
    except ValidationError as err:
        logger.error("Failed to create card. Validation error.")
        for field, error in err.messages.items():
            logger.error(f"Invalid field '{field}'. {error}")
            errors.add(f"invalid.{field}", error)

    if not errors.is_empty():
        return errors.done(400, ERROR_BAD_REQUEST)

    try:
        result = await cards.create_card(app=request.app, msg=message)
    except ErrorTitleAlreadyExists:
        return errors.done(404, ERROR_TITLE_ALREADY_EXISTS)
    except ErrorBordNotFound:
        return errors.done(404, ERROR_BOARD_NOT_FOUND)
    except ErrorStatusNotFound:
        return errors.done(404, ERROR_STATUS_NOT_FOUND)
    except ErrorPriorityNotFound:
        return errors.done(404, ERROR_PRIORITY_NOT_FOUND)
    except ErrorDeveloperNotFound:
        return errors.done(404, ERROR_DEVELOPER_NOT_FOUND)
    except ErrorDatabase:
        return errors.done(500, ERROR_DATABASE)
    except Exception as err:
        logger.error(f"Failed to create card. {type(err)}: {err}")
        return errors.done(500, ERROR_UNKNOWN)

    return web.json_response({
         "id": str(result.card_id),
         "created_at": round(result.created_at.timestamp())
        })
