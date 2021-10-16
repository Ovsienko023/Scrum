from aiohttp.web import middleware
from app.http.constants import REQUEST_TOKEN


@middleware
async def check_token(request, handler):
    request[REQUEST_TOKEN] = None
    query = dict(request.query)

    if query.get("token"):
        request[REQUEST_TOKEN] = query.get("token")

    if request.headers.get('Authorization'):
        token = request.headers.get('Authorization').replace("Bearer ", "")
        request[REQUEST_TOKEN] = token

    resp = await handler(request)

    return resp

