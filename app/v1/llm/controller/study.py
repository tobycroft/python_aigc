import os

from flask import Blueprint

from tuuz import Ret,Input,Database

Controller = Blueprint(os.path.splitext(os.path.basename(__file__))[0], __name__)


@Controller.before_request
def before():
    token = Input.Header.String("token")
    data = Database.Db().table("ai_project").whereRow('token', token).find()
    if data is None:
        return Ret.fail(400, 'project未启用')
    pass
@Controller.post('/')
def slash():
    return "/"



@Controller.post('/text')
async def text():
    # 加载tokenizer

    return Ret.success(0, )
