import asyncio
from aiohttp import web

from internal.container.container import container
from internal.container import DI_CONFIG, DI_LOGGER, DI_DATABASE_CLIENT
from app.constants import APP_CONTAINER
from app.http.routes import setup_routes


async def init_app(cnt) -> web.Application:
    app = web.Application()

    client = cnt.resolve(DI_DATABASE_CLIENT)
    client.connect()

    app[APP_CONTAINER] = cnt
    app.add_routes(setup_routes())

    return app


def main():
    config = container.resolve(DI_CONFIG)

    app = init_app(cnt=container)
    logger = container.resolve(DI_LOGGER)

    web.run_app(app, host=config["db"]["host"], port=config["db"]["port"], access_log=logger)
