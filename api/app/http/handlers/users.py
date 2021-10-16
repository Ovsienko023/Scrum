from aiohttp import web
from marshmallow import ValidationError

from internal.database.errors import ErrorDatabase
from internal.container.constants import DI_LOGGER
from app.constants import APP_CONTAINER
from app.http.constants import ERROR_BAD_REQUEST, ERROR_UNKNOWN, ERROR_DATABASE
from app.http.schemas.users import SchemaCreateUser
from app.http.errors import ErrorContainer
from app.native.users import (
    users,
    MessageCreateUser,
    ERROR_LOGIN_ALREADY_EXISTS,
    ErrorLoginAlreadyExists,
)


async def create_users(request):
    errors = ErrorContainer()
    container = request.app[APP_CONTAINER]
    logger = container.resolve(DI_LOGGER)

    try:
        data = await request.json()
    except ValueError as err:
        logger.error(f"Failed to create user.  ValueError: {err}")
        return errors.done(400, ERROR_BAD_REQUEST)

    schema = SchemaCreateUser()

    try:
        message = MessageCreateUser(**schema.load(data))
    except ValidationError as err:
        logger.error("Failed to create user. Validation error.")
        for field, error in err.messages.items():
            logger.error(f"Invalid field '{field}'. {error}")
            errors.add(f"invalid.{field}", error)
        return errors.done(400, ERROR_BAD_REQUEST)

    try:
        results = await users.create_user(app=request.app, msg=message)
    except ErrorLoginAlreadyExists:
        return errors.done(400, ERROR_LOGIN_ALREADY_EXISTS)
    except ErrorDatabase:
        return errors.done(500, ERROR_DATABASE)
    except Exception as err:
        logger.error(f"Failed to create user: {(type(err))}, {err}")
        return errors.done(500, ERROR_UNKNOWN)

    return web.json_response({
            "id": str(results.user_id),
            "created_at": round(results.created_at.timestamp()),
        })
