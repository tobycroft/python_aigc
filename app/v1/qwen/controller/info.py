import os

from flask import Blueprint

from app.v1.qwen.model.QianwenModel import QianwenModel
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


@Controller.post('/list')
def list():
    uid = Header.Int('uid')
    data = QianwenModel().api_select_byUid(uid)
    return Ret.success(data=data)


# update
@Controller.post('/update')
def update():
    uid = Header.Int('uid')
    id = Post.Int('id')
    name = Post.Str('name')
    key = Post.Str('key')
    rid = Post.Int('rid')
    model = Post.Str('model')
    QianwenModel().api_update_byUidAndId(uid, id, name, key, rid, model)


# delete
@Controller.post('/delete')
def delete():
    uid = Header.Int('uid')
    id = Post.Int('id')
    if QianwenModel().api_delete_byUidAndId(uid, id):
        return Ret.success()
    else:
        return Ret.fail(500, echo='QianwenModel删除失败')


# add
@Controller.post('/add')
def add():
    uid = Header.Int('uid')
    id = Post.Int('id')
    name = Post.Str('name')
    key = Post.Str('key')
    rid = Post.Int('rid')
    model = Post.Str('model')
    if QianwenModel().api_insert(uid, id, name, key, rid, model):
        return Ret.success()
    else:
        return Ret.fail(500, echo='QianwenModel添加失败')


# get
@Controller.post('get')
def get():
    uid = Header.Int('uid')
    id = Post.Int('id')
    data = QianwenModel().api_find_byUidAndId(uid, id)
    if data is None:
        return Ret.fail(404, echo='数据不存在')
    return Ret.success(data=data)
