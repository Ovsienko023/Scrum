import asyncio
from aiohttp import web

from app.http.routes import setup_routes


async def init_app(cnt) -> web.Application:
    app = web.Application()
    app.add_routes(setup_routes())

    return app


def main():
    asyncio.run(init_app(cnt=""))
    app = init_app(cnt="")

    web.run_app(app, host="127.0.0.1", port=8888)  # access_log=logger
