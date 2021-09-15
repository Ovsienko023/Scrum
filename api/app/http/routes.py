from aiohttp import web
from app.http.handlers import users, boards, cards


def setup_routes():
    return [
        web.post("/users", users.create_users),
        web.post("/boards", boards.create_board),
        web.post("/cards", cards.create_card),
    ]
