from aiohttp import web


async def create_users(request):
    try:
        data = await request.json()
    except ValueError as err:
        pass
    print("create user", data)
        # logger.error(f"Failed to create user.  ValueError: {err}")
        # return errors.done(400, ERROR_BAD_REQUEST)
    return web.json_response({"key": "Hello"})


