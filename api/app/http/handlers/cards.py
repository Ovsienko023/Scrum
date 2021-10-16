from aiohttp import web
from marshmallow import ValidationError

from internal.database.errors import ErrorDatabase
from internal.container.constants import DI_LOGGER
from app.constants import APP_CONTAINER
from app.http.auth import authorization
from app.http.constants import ERROR_BAD_REQUEST, ERROR_UNKNOWN, ERROR_DATABASE
from app.http.schemas.cards import SchemaGetCard, SchemaCreateCard, SchemaUpdateCard, SchemaGetReport, SchemaRemoveCard
from app.http.errors import ErrorContainer
from app.native.cards import (
    cards,
    MessageGetCard,
    MessageCreateCard,
    MessageUpdateCard,
    MessageGetReport,
    MessageRemoveCard,
    ErrorCardIdNotFound,
    ErrorBordNotFound,
    ErrorStatusNotFound,
    ErrorPriorityNotFound,
    ErrorDeveloperNotFound,
    ERROR_BOARD_NOT_FOUND,
    ERROR_STATUS_NOT_FOUND,
    ERROR_PRIORITY_NOT_FOUND,
    ERROR_DEVELOPER_NOT_FOUND,
    ERROR_CARD_ID_NOT_FOUND,
)


@authorization
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
            "estimates_time": str(result.estimates_time),
            "board_id": str(result.board_id),
            "creator_id": str(result.creator_id),
            "created_at": round(result.created_at.timestamp()),
            "updated_at": round(result.updated_at.timestamp())
    })


async def get_report(request) -> web.Response:
    errors = ErrorContainer()
    container = request.app[APP_CONTAINER]
    logger = container.resolve(DI_LOGGER)

    data = dict(request.match_info)

    schema = SchemaGetReport()

    try:
        message = MessageGetReport(**schema.load(data))
    except ValidationError as err:
        logger.error("Failed to get report. Validation error.")
        for field, error in err.messages.items():
            logger.error(f"Invalid field '{field}'. {error}")
            errors.add(f"invalid.{field}", error)

        return errors.done(400, ERROR_BAD_REQUEST)

    try:
        result = await cards.get_report(app=request.app, msg=message)
    except ErrorCardIdNotFound:
        return errors.done(404, ERROR_CARD_ID_NOT_FOUND)
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
        logger.error(f"Failed to get report. {type(err)}: {err}")
        return errors.done(500, ERROR_UNKNOWN)

    return web.json_response({
        "count": len(result.cards),
        "estimation": result.estimation.hours_to_string(),
        "cards": [
            {
                "title": card.title,
                "description": card.description,
                "developer_id": str(card.developer_id),
                "priority": card.priority,
                "status": card.status,
                "estimates_time": str(card.estimates_time),
                "board_id": str(card.board_id),
                "creator_id": str(card.creator_id),
                "created_at": round(card.created_at.timestamp()),
                "updated_at": round(card.updated_at.timestamp())
            }
            for card in result.cards
        ]
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

        return errors.done(400, ERROR_BAD_REQUEST)

    try:
        result = await cards.create_card(app=request.app, msg=message)
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


async def update_card(request) -> web.Response:
    errors = ErrorContainer()
    container = request.app[APP_CONTAINER]
    logger = container.resolve(DI_LOGGER)

    try:
        data = await request.json()
        data["card_id"] = request.match_info["card_id"]
    except (ValueError, KeyError) as err:
        logger.error(f"Failed to update card.  ValueError: {err}")
        return errors.done(400, ERROR_BAD_REQUEST)

    schema = SchemaUpdateCard()

    try:
        message = MessageUpdateCard(**schema.load(data))
    except ValidationError as err:
        logger.error("Failed to update card. Validation error.")
        for field, error in err.messages.items():
            logger.error(f"Invalid field '{field}'. {error}")
            errors.add(f"invalid.{field}", error)

        return errors.done(400, ERROR_BAD_REQUEST)

    try:
        await cards.update_card(app=request.app, msg=message)
    except ErrorCardIdNotFound:
        return errors.done(404, ERROR_CARD_ID_NOT_FOUND)
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
        logger.error(f"Failed to update card. {type(err)}: {err}")
        return errors.done(500, ERROR_UNKNOWN)

    return web.json_response()


async def remove_card(request) -> web.Response:
    errors = ErrorContainer()
    container = request.app[APP_CONTAINER]
    logger = container.resolve(DI_LOGGER)

    data = {"card_id":  request.match_info.get("card_id")}

    schema = SchemaRemoveCard()

    try:
        message = MessageRemoveCard(**schema.load(data))
    except ValidationError as err:
        logger.error("Failed to remove card. Validation error.")
        for field, error in err.messages.items():
            logger.error(f"Invalid field '{field}'. {error}")
            errors.add(f"invalid.{field}", error)

        return errors.done(400, ERROR_BAD_REQUEST)

    try:
        await cards.remove_card(app=request.app, msg=message)
    except ErrorCardIdNotFound:
        return errors.done(404, ERROR_CARD_ID_NOT_FOUND)
    except ErrorDatabase:
        return errors.done(500, ERROR_DATABASE)
    except Exception as err:
        logger.error(f"Failed to remove card. {type(err)}: {err}")
        return errors.done(500, ERROR_UNKNOWN)

    return web.json_response()
