import os

from flask import Blueprint

import Database
from app.v1.user.model import UserModel
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
    # print(Database.Db().table('ai_user').insert({
    #     'username': username,
    #     'password': password,
    # }))
    # print(Database.Db().table('ai_user').whereRow('username', username).update({
    #     'password': password,
    # }))
    # print(Database.Db().table('ai_user').whereRow('username', username).select())
    return Ret.success(0, UserModel.Api_find_byUsername(username))

#
# async def login():
#     username = Input.Post.String('username')
#     password = Input.Post.String("password")
#     if len(username) < 1:
#         return Ret.fail(400, None, '用户名不能为空')
#     if Database.Db().table('ai_user').insert({
#         'username': username,
#         'password': password,
#     }) is None:
#         return Ret.fail(400, None, '注册失败')
#     return Ret.success(0, )