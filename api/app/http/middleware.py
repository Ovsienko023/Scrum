import jwt
from hashlib import sha256

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

    # if query.get("token") or request.headers.get('Authorization'):
    resp = await handler(request)

    return resp

# def response(self) -> web.Response:
#     return web.json_response(
#         status=self.code,
#         data={
#             "error": {
#                 "code": self.code,
#                 "description": self.description,
#                 "details": self.details
#             }
#         }
#     )

# access_token = ""
#
# decoded = jwt.decode(access_token, "secret", algorithms=["HS256"])
# print(decoded)
#
# password_hash = sha256("admin".encode("utf-8")).hexdigest()
# print(password_hash)
