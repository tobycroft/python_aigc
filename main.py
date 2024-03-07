import config.app
import config.db
import tuuz.Redis.pyredis
import tuuz.database.db
from router.router import MainRoute

config.app.init()
tuuz.Database.db.init()
tuuz.Redis.pyredis.init()

app = MainRoute()

app.run(host="0.0.0.0", port=80, debug=True)
