import os

from flask import Blueprint

import Database
from tuuz import Database, Input, Ret

Controller = Blueprint(os.path.splitext(os.path.basename(__file__))[0], __name__)


@Controller.before_request
def before():
    pass


@Controller.post('/')
def slash():
    return "/"


@Controller.post('/register')
async def register():
    username = Input.Post.String('username')
    password = Input.Post.String("password")
    if len(username) < 1:
        return Ret.fail(400, None, '用户名不能为空')
    print(Database.Db().table('ai_user').insertGetId({
        'username': username,
        'password': password,
    }))
    # print(Database.Db().table('ai_user').whereRow('username', username).update({
    #     'password': password,
    # }))
    # print(Database.Db().table('ai_user').whereRow('username', username).select())
    # print(Database.Db().table('ai_user').whereRow('username', username).find())
    return Ret.success(0, )
