import asyncio
from aiohttp import web

from internal.container.container import container
from internal.container import DI_LOGGER, DI_DATABASE_CLIENT
from app.constants import APP_CONTAINER
from app.http.routes import setup_routes


async def init_app(cnt) -> web.Application:
    app = web.Application()
    app.on_cleanup.append(close_database)

    client = cnt.resolve(DI_DATABASE_CLIENT)
    await client.connect()

    app[APP_CONTAINER] = cnt
    app.add_routes(setup_routes())

    return app


def main():
    logger = container.resolve(DI_LOGGER)

    app = init_app(cnt=container)
    web.run_app(app, host="127.0.0.1", port=8888, access_log=logger)


async def close_database(app: web.Application):
    cnt = app[APP_CONTAINER]
    database = cnt.resolve(DI_DATABASE_CLIENT)
    await database.close()
