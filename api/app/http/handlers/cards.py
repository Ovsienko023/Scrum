from aiohttp import web
from marshmallow import ValidationError

from internal.database.errors import ErrorDatabase
from internal.container.constants import DI_LOGGER
from app.constants import APP_CONTAINER, ERROR_BAD_REQUEST, ERROR_UNKNOWN, ERROR_DATABASE
from app.http.schemas.cards import SchemaCreateCard
from app.http.errors import ErrorContainer
from app.native.cards import cards, MessageCreateCard


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
    except ErrorDatabase:
        return errors.done(500, ERROR_DATABASE)
    except Exception as err:
        logger.error(f"Failed to create card. {type(err)}: {err}")
        return errors.done(500, ERROR_UNKNOWN)

    return web.json_response({
         "id": str(result.card_id),
         "created_at": round(result.created_at.timestamp())
        })
