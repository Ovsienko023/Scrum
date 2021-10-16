import time
from hashlib import sha256

import jwt
from aiohttp import web

from internal.database.errors import ErrorDatabase
from internal.container import DI_DATABASE_CLIENT, DI_LOGGER
from app.constants import APP_CONTAINER
from app.native.oauth import (
    MessageGetToken,
    MessageToken,
    ErrorLoginNotFound,
    ErrorWrongPassword,
)


async def get_token(app: web.Application, msg: MessageGetToken) -> MessageToken:
    container = app[APP_CONTAINER]
    client = container.resolve(DI_DATABASE_CLIENT)
    logger = container.resolve(DI_LOGGER)

    password_hash = sha256(msg.login.encode("utf-8")).hexdigest()

    query = """
        select *
        from oauth.get_token(
            %(login)s,
            %(password)s
        )
    """
    params = {
        "login": msg.login,
        "password": password_hash,
    }
    try:
        result = await client.fetchone(query, params)
    except Exception as err:
        logger.error(f"Failing to database: {type(err)}, {err}")
        raise ErrorDatabase

    error = result.get("error")
    if error is not None:
        logger.error(f"Failing to get token: {error}")
        if error["reason"] == "not_found" and error["description"] == "_login":
            raise ErrorLoginNotFound
        if error["reason"] == "not_found" and error["description"] == "_password":
            raise ErrorWrongPassword
        raise ErrorDatabase

    data = {
        "user_id": str(result.get("user_id")),
    }
    jwt_token = jwt.encode(data, "secret", algorithm="HS256")

    return MessageToken(
        access_token=jwt_token
    )
