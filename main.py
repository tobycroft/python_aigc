from asyncio import run, create_task

from sanic import json

import config.app
import config.db

run(config.app.init())

import tuuz.Redis.pyredis
import tuuz.database.db
from router.router import main_route

from tuuz.Calc import Token


async def main():
    _ = create_task(Token.refresh_base_num())
    _ = create_task(tuuz.database.db.init())
    _ = create_task(tuuz.Redis.pyredis.init())


app = main_route()


@app.route('/')
async def index(request):
    return json('Hello, World!')


if __name__ == '__main__':
    run(main())
    app.run(host="0.0.0.0", port=84, debug=True)
