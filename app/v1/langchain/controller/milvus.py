import os

from flask import Blueprint

import tuuz.Database
import tuuz.Input
import tuuz.Ret

Controller = Blueprint(os.path.splitext(os.path.basename(__file__))[0], __name__)


@Controller.post('/')
def slash():
    return Controller.name


@Controller.before_request
def before():
    token = tuuz.Input.Header.String("token")
    data = tuuz.Database.Db().table("ai_project").whereRow('token', token).find()
    if data is None:
        return tuuz.Ret.fail(400, 'project未启用')
    pass


@Controller.post('/text')
async def text():
    return tuuz.Ret.success(0, )
