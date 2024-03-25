from asyncio import run

import config.app
import config.db
import tuuz.Redis.pyredis
import tuuz.database.db
from router.router import MainRoute

run(config.app.init())
run(tuuz.database.db.init())
run(tuuz.Redis.pyredis.init())

app = MainRoute()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=84, debug=True)
