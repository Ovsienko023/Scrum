from aiohttp import web
import asyncio

from app.http.routes.routes import setup_routes


def main():
    app = web.Application()
    app.add_routes(setup_routes())
    web.run_app(app, host="127.0.0.1", port=8888)  # access_log=logger
