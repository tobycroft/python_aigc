import os

from flask import Blueprint, request

from app.v1.user.model import UserModel, TokenModel
from tuuz import Input, Ret
from tuuz.Calc import Encrypt, Token

Controller = Blueprint(os.path.splitext(os.path.basename(__file__))[0], __name__)


@Controller.before_request
def before():
    pass


@Controller.post('/')
def slash():
    return "/"


@Controller.post('/test')
async def test():
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


@Controller.post('/login')
async def login():
    username = Input.Post.String('username')
    password = Input.Post.String("password")
    user = UserModel.Api_find_byUsernameAndPassword(username, password)
    if user is None:
        return Ret.fail(404, None, '用户名或密码错误')
    token = Token.generate_token()
    if TokenModel.Api_insert(user["id"], token, request.remote_addr):
        return Ret.success(0, {"uid": user["id"], "token": token, 'username': user['username']})
    else:
        return Ret.fail(500, None, '登录失败')


@Controller.post('/phone')
async def phone():
    return Ret.success(0)


@Controller.post('/register')
async def register():
    username = Input.Post.String('username')
    password = Input.Post.String("password")
    if len(username) < 1:
        return Ret.fail(400, None, '用户名不能为空')
    if UserModel.Api_find_byUsername(username) is not None:
        return Ret.fail(409, None, '用户名已被注册')
    if UserModel.Api_insert(username, Encrypt.md5(password)):
        return Ret.success(0, UserModel.Api_find_byUsername(username))
    else:
        return Ret.fail(500, None, '注册失败')
