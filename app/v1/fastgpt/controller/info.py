import os

from flask import Blueprint

from app.v1.fastgpt.model.FastgptModel import FastgptModel
from common.controller.LoginController import LoginedController
from tuuz import Ret
from tuuz.Input import Header, Post

Controller = Blueprint(os.path.splitext(os.path.basename(__file__))[0], __name__)


@Controller.post('/')
def slash():
    return Controller.name


@Controller.before_request
def before_request():
    return LoginedController()


# list
@Controller.post('/list')
def list():
    uid = Header.Int('uid')
    data = FastgptModel().api_select_byUid(uid)
    return Ret.success(data=data)


# update
@Controller.post('/update')
def update():
    uid = Header.Int('uid')
    id = Post.Int('id')
    name = Post.Str('name')
    key = Post.Str('key')
    base_url = Post.Str('base_url')
    if FastgptModel().api_update_nameAndKeyAndBaseUrl_byUidAndId(uid, id, name, key, base_url):
        return Ret.success()
    else:
        return Ret.fail(500, echo='FastgptModel更新失败')


# delete
@Controller.post('/delete')
def delete():
    uid = Header.Int('uid')
    id = Post.Int('id')
    if FastgptModel().api_delete_byUidAndId(uid, id):
        return Ret.success()
    else:
        return Ret.fail(500, echo='FastgptModel删除失败')


# add
@Controller.post('/add')
def add():
    uid = Header.Int('uid')
    name = Post.Str('name')
    team_id = Post.Int('team_id')
    key = Post.Str('key')
    base_url = Post.Str('base_url')
    model = Post.Str('model')
    detail = Post.Int('detail')
    if FastgptModel().api_insert(uid, name, team_id, key, base_url, model, detail):
        return Ret.success()
    else:
        return Ret.fail(500, echo='FastgptModel添加失败')


# get
@Controller.post('/get')
def get():
    uid = Header.Int('uid')
    id = Post.Int('id')
    data = FastgptModel().api_find_byUidAndId(uid, id)
    if data is None:
        return Ret.fail(404, echo='FastgptModel获取失败')
    return Ret.success(data=data)
