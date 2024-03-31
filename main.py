from asyncio import run, create_task

from apscheduler.schedulers.background import BackgroundScheduler

import config.app
import config.db
from tuuz.Calc import Token

run(config.app.init())

import tuuz.Redis.pyredis
import tuuz.database.db
from router.router import MainRoute


async def main():
    _ = create_task(tuuz.database.db.init())
    _ = create_task(tuuz.Redis.pyredis.init())


app = MainRoute()


@app.route('/')
def index():
    return 'AIGC'


if __name__ == "__main__":
    run(main())
    sch = BackgroundScheduler()
    sch.remove_all_jobs()
    sch.add_job(Token.refresh, 'interval', seconds=1, replace_existing=True, )
    if not sch.running:
        sch.start()
    # app.run(host="0.0.0.0", port=84, debug=config.app.TestMode, threaded=True)
    app.run(host='0.0.0.0', port=84, debug=True, threaded=True)
