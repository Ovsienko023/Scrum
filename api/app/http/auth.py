from functools import wraps

import jwt
from aiohttp import web

from app.http.constants import REQUEST_TOKEN, PUBLIC_KEY


def authorization(func):
    @wraps(func)
    def wrapper(request):

        if request[REQUEST_TOKEN]:
            decoded = jwt.decode(request[REQUEST_TOKEN], PUBLIC_KEY, algorithms=["HS256"])
            if decoded.get("user_id"):
                return func(request)

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
