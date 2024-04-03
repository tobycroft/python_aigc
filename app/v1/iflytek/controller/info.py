import os

from flask import Blueprint

from app.v1.iflytek.model.IflytekModel import IflytekModel
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
    data = IflytekModel().api_select_byUid(uid)
    return Ret.success(data=data)


# update
@Controller.post('/update')
def update():
    # uid, id, name, team_id, host, app_secret, app_id, app_key, vcn
    uid = Header.Int('uid')
    id = Post.Int('id')
    name = Post.Str('name')
    team_id = Post.Int('team_id')
    host = Post.Str('host')
    app_secret = Post.Str('app_secret')
    app_id = Post.Str('app_id')
    app_key = Post.Str('app_key')
    vcn = Post.Str('vcn')
    if IflytekModel().api_update_byUidAndId(uid, id, name, team_id, host, app_secret, app_id, app_key, vcn):
        return Ret.success()
    else:
        return Ret.fail(500, echo='IflytekModel更新失败')


# delete
@Controller.post('/delete')
def delete():
    uid = Header.Int('uid')
    id = Post.Int('id')
    if IflytekModel().api_delete_byUidAndId(uid, id):
        return Ret.success()
    else:
        return Ret.fail(500, echo='IflytekModel删除失败')


# add
@Controller.post('/add')
def add():
    # uid, name, team_id, host, app_secret, app_id, app_key, vcn
    uid = Header.Int('uid')
    name = Post.Str('name')
    team_id = Post.Int('team_id')
    host = Post.Str('host')
    app_secret = Post.Str('app_secret')
    app_id = Post.Str('app_id')
    app_key = Post.Str('app_key')
    vcn = Post.Str('vcn')
    if IflytekModel().api_insert(uid, name, team_id, host, app_secret, app_id, app_key, vcn):
        return Ret.success()
    else:
        return Ret.fail(500, echo='IflytekModel添加失败')


# get
@Controller.post('get')
def get():
    uid = Header.Int('uid')
    id = Post.Int('id')
    data = IflytekModel().api_find_byUidAndId(uid, id)
    if data is None:
        return Ret.fail(404, echo='数据不存在')
    return Ret.success(data=data)
