from aiohttp import web
from marshmallow import ValidationError

from internal.database.errors import ErrorDatabase
from internal.container.constants import DI_LOGGER
from app.constants import APP_CONTAINER
from app.http.constants import ERROR_BAD_REQUEST, ERROR_UNKNOWN, ERROR_DATABASE
from app.http.schemas.oauth import SchemaGetToken
from app.http.errors import ErrorContainer
from app.native.oauth import (
    oauth,
    MessageGetToken,
    ERROR_LOGIN_NOT_FOUND,
    ERROR_WRONG_PASSWORD,
    ErrorLoginNotFound,
    ErrorWrongPassword,
)


async def get_token(request):
    errors = ErrorContainer()
    container = request.app[APP_CONTAINER]
    logger = container.resolve(DI_LOGGER)

    try:
        data = await request.json()
    except ValueError as err:
        logger.error(f"Failed to get token.  ValueError: {err}")
        return errors.done(400, ERROR_BAD_REQUEST)

    schema = SchemaGetToken()

    try:
        message = MessageGetToken(**schema.load(data))
    except ValidationError as err:
        logger.error("Failed to get token. Validation error.")
        for field, error in err.messages.items():
            logger.error(f"Invalid field '{field}'. {error}")
            errors.add(f"invalid.{field}", error)
        return errors.done(400, ERROR_BAD_REQUEST)

    try:
        results = await oauth.get_token(app=request.app, msg=message)
    except ErrorWrongPassword:
        return errors.done(400, ERROR_WRONG_PASSWORD)
    except ErrorLoginNotFound:
        return errors.done(404, ERROR_LOGIN_NOT_FOUND)
    except ErrorDatabase:
        return errors.done(500, ERROR_DATABASE)
    except Exception as err:
        logger.error(f"Failed to get token: {(type(err))}, {err}")
        return errors.done(500, ERROR_UNKNOWN)

    return web.json_response({
            "token": results.access_token
        })
