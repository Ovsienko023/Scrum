from functools import wraps

from aiohttp import web

from app.http.constants import REQUEST_TOKEN, REQUEST_USER_ID
from app.native.oauth import oauth
from internal.container.container import container
from internal.container import DI_LOGGER


def authorization(func):
    @wraps(func)
    async def wrapper(request):

        if request[REQUEST_TOKEN]:
            try:
                request[REQUEST_USER_ID] = await oauth.resolve_user(app=request.app, token=request[REQUEST_TOKEN])
                return await func(request)
            except Exception as err:
                logger = container.resolve(DI_LOGGER)
                logger.error(f"Error authorization {type(err)}, {err}")

        return web.json_response(
            status=401,
            data={
                "error": {
                    "code": 401,
                    "description": "Permission denied",
                    "details": [],
                }
            }
        )

    return wrapper
