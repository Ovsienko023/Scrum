from aiohttp import web
from app.http.handlers import users, boards, cards


def setup_routes():
    return [
        web.post("/users", users.create_users),
        web.get("/boards/{board_id}", boards.get_board),
        web.post("/boards", boards.create_board),
        web.get("/cards/{card_id}", cards.get_card),
        web.patch("/cards/{card_id}", cards.update_card),
        web.post("/cards", cards.create_card),
    ]
