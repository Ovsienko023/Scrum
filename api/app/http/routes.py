from aiohttp import web
from app.http.handlers.users import create_users


def setup_routes():
    return [
        web.post('/users', create_users),
    ]
