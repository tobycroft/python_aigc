from asyncio import run, create_task

import config.app
import config.db

run(config.app.init())

import tuuz.Redis.pyredis
import tuuz.database.db
from router.router import MainRoute
from tuuz.Calc import Token


async def main():
    _ = create_task(Token.refresh_base_num())
    _ = create_task(tuuz.database.db.init())
    _ = create_task(tuuz.Redis.pyredis.init())


if __name__ == "__main__":
    run(main())
    app = MainRoute()
    app.run(host="0.0.0.0", port=84, debug=True)
