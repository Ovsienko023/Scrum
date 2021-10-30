from aiohttp import web
from pathlib import Path
from aiohttp_swagger3 import SwaggerFile, SwaggerUiSettings

from internal.container.container import container
from internal.container import DI_LOGGER, DI_DATABASE_CLIENT, DI_CONFIG
from app.constants import APP_CONTAINER
from app.http.routes import setup_routes
from app.http.middleware import check_token


async def init_app(cnt) -> web.Application:
    config = cnt.resolve(DI_CONFIG)
    app = web.Application(middlewares=[check_token])

    app.on_cleanup.append(close_database)

    client = cnt.resolve(DI_DATABASE_CLIENT)
    await client.connect()

    app[APP_CONTAINER] = cnt
    app.add_routes(setup_routes())

    if config["docs"]["enable"]:
        SwaggerFile(
            app,
            spec_file=Path(config["dirs"]["docs"]),
            swagger_ui_settings=SwaggerUiSettings(path=config["docs"]["url"]),
        )

    return app


def main():
    logger = container.resolve(DI_LOGGER)
    config = container.resolve(DI_CONFIG)

    app = init_app(cnt=container)
    web.run_app(app, host="127.0.0.1", port=config["web"]["port"], access_log=logger)


async def close_database(app: web.Application):
    cnt = app[APP_CONTAINER]
    database = cnt.resolve(DI_DATABASE_CLIENT)
    await database.close()
