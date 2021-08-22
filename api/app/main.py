import asyncio
from aiohttp import web

from internal.container.container import container
from internal.container.constants import DI_CONFIG, DI_LOGGER
from app.http.routes import setup_routes


async def init_app(cnt) -> web.Application:
    app = web.Application()
    app.add_routes(setup_routes())

    return app


def main():
    config = container.resolve(DI_CONFIG)

    app = init_app(cnt="")
    logger = container.resolve(DI_LOGGER)

    web.run_app(app, host=config["db"]["host"], port=config["db"]["port"], access_log=logger)
