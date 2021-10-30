from aiohttp import web


async def fetch_echo(request) -> web.Response:
    return web.json_response({
        "success": "Hello api!"
    })
