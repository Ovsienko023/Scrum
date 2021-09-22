from aiohttp import web

from internal.database.errors import ErrorDatabase
from internal.container.constants import DI_LOGGER
from app.constants import APP_CONTAINER, ERROR_UNKNOWN, ERROR_DATABASE
from app.http.errors import ErrorContainer
from app.native.statuses import (
    statuses,

)


async def get_statuses(request) -> web.Response:
    errors = ErrorContainer()
    container = request.app[APP_CONTAINER]
    logger = container.resolve(DI_LOGGER)

    try:
        result = await statuses.get_statuses(app=request.app)
    except ErrorDatabase:
        return errors.done(500, ERROR_DATABASE)
    except Exception as err:
        logger.error(f"Failed to get statuses. {type(err)}: {err}")
        return errors.done(500, ERROR_UNKNOWN)

    return web.json_response({
        "count": result.count,
        "statuses": [
            {
                "id": str(status.status_id),
                "title": status.title,
            }
            for status in result.statuses
        ]
    })
