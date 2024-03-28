import threading
from asyncio import run

import config.app
import config.db

run(config.app.init())

import tuuz.Redis.pyredis
import tuuz.database.db
from router.router import MainRoute
from tuuz.Calc import Token

if __name__ == "__main__":
    threading.Thread(target=Token.refresh_base_num).start()
    run(tuuz.database.db.init())
    run(tuuz.Redis.pyredis.init())
    app = MainRoute()
    app.run(host="0.0.0.0", port=84, debug=True)
