from aiohttp.web import middleware
from app.http.constants import REQUEST_TOKEN, REQUEST_USER_ID
from app.native.oauth import oauth
from internal.container.container import container
from internal.container import DI_LOGGER


@middleware
async def check_token(request, handler):
    if "/docs" or "/oauth" in request.path:
        return await handler(request)

    token = None
    request[REQUEST_USER_ID] = None
    query = dict(request.query)

    if query.get("token"):
        token = query.get("token")

    if request.headers.get("Authorization"):
        token = request.headers.get("Authorization").replace("Bearer ", "")

    try:
        request[REQUEST_USER_ID] = await oauth.resolve_user(app=request.app, token=token)
    except Exception as err:
        logger = container.resolve(DI_LOGGER)
        logger.error(f"Error resolve user_id {type(err)}, {err}")

    return await handler(request)

