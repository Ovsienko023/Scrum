from functools import wraps

from aiohttp import web

from app.http.constants import REQUEST_USER_ID


def authorization(func):
    @wraps(func)
    async def wrapper(request: web.Request):
        if request[REQUEST_USER_ID]:
            return await func(request)

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
