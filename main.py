import config.app
import config.db
import tuuz
import Redis.pyredis
import database.db
from router.router import MainRoute

config.app.init()
tuuz.database.db.init()
tuuz.Redis.pyredis.init()

app = MainRoute()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=84, debug=True)
