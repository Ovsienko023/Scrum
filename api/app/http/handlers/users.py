from aiohttp import web
from marshmallow import ValidationError
from internal.container.constants import DI_LOGGER
from app.constants import APP_CONTAINER, ERROR_BAD_REQUEST, ERROR_UNKNOWN
from app.http.schemas.users import SchemaCreateUser
from app.http.errors import ErrorContainer
from app.native.users import (
    users,
    MessageCreateUser
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

    if not errors.is_empty():
        return errors.done(400, ERROR_BAD_REQUEST)

    try:
        results = users.create_user(app=request.app, msg=message)
    except Exception as err:
        logger.error(f"{err}")
        errors.done(500, ERROR_UNKNOWN)

    return web.json_response(results.get_entity())