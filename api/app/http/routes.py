from aiohttp import web
from app.http.handlers import users, boards, cards, priorities, statuses, oauth


def setup_routes():
    return [
        web.post("/oauth", oauth.get_token),
        web.post("/users", users.create_users),

        web.post("/boards", boards.create_board),
        web.get("/boards", boards.get_boards),
        web.get("/boards/{board_id}", boards.get_board),
        web.patch("/boards/{board_id}", boards.update_board),
        web.delete("/boards/{board_id}", boards.remove_board),

        web.get("/cards/report", cards.get_report),
        web.post("/cards", cards.create_card),
        web.get("/cards/{card_id}", cards.get_card),
        web.patch("/cards/{card_id}", cards.update_card),
        web.delete("/cards/{card_id}", cards.remove_card),

        web.get("/misc/priorities", priorities.get_priorities),
        web.get("/misc/statuses", statuses.get_statuses),
    ]
