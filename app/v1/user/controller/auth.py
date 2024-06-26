import os

from flask import Blueprint

from app.v1.user.model.UserModel import UserModel
from common.model.TokenModel import TokenModel
from tuuz import Input, Ret, Database
from tuuz.Calc import Token, Encrypt

Controller = Blueprint(os.path.splitext(os.path.basename(__file__))[0], __name__)


@Controller.before_request
def before():
    pass


@Controller.post('/')
def slash():
    return Controller.name


@Controller.post('/login')
async def login():
    username = Input.Post.String('username')
    password = Input.Post.String("password")
    user = UserModel().api_find_byUsernameAndPassword(username, password)
    if user is None:
        return Ret.fail(404, None, '用户名或密码错误')
    token = Token.generate_token()
    if TokenModel().Api_insert(user["id"], token, Input.ip()):
        return Ret.success(0, {"uid": user["id"], "token": token, 'username': user['username']})
    else:
        return Ret.fail(500, None, '登录失败')


@Controller.post('/phone')
async def phone():
    # todo: 发送验证码
    phone = Input.Post.String('phone')
    code = Input.Post.String('code')
    if len(phone) < 1:
        return Ret.fail(400, None, '手机号不能为空')
    if len(code) < 1:
        return Ret.fail(400, None, '验证码不能为空')
    return Ret.success(0)


@Controller.post('/register')
async def register():
    username = Input.Post.String('username')
    password = Input.Post.String("password")
    if len(username) < 1:
        return Ret.fail(400, None, '用户名不能为空')
    if UserModel().api_find_byUsername(username) is not None:
        return Ret.fail(409, None, '用户名已被注册')
    db = Database.Db().get_connection()
    db.begin()
    id = UserModel(db).api_insert(username, Encrypt.md5(password))
    if not id:
        db.rollback()
        db.close()
        return Ret.fail(500, None, '注册失败')
    user = UserModel(db).api_find_limit_byUsername(id)
    if not user:
        db.rollback()
        db.close()
        return Ret.fail(500, None, '未找到用户')
    token = Token.generate_token()
    if not TokenModel(db).Api_insert(user["id"], token, Input.ip()):
        db.rollback()
        db.close()
        return Ret.fail(500, None, 'token失败')
    db.commit()
    db.close()
    return Ret.success(0, {"uid": user["id"], "token": token, 'username': user['username']})
