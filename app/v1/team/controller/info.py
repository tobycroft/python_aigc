import os

from flask import Blueprint

from app.v1.team.model.TeamModel import TeamModel
from common.controller.LoginController import LoginedController
from tuuz import Ret, Input, Database

Controller = Blueprint(os.path.splitext(os.path.basename(__file__))[0], __name__)


@Controller.before_request
def before():
    return LoginedController()


@Controller.post('/')
def slash():
    return "/"


@Controller.post('create')
async def create():
    uid = Input.Header.Int("uid")
    name = Input.Post.Str("name")
    # if name len should be > 1
    if len(name) < 1:
        return Ret.fail(400, echo="name应该大于1")
    if TeamModel().api_find_byUidAndName(uid, name):
        return Ret.fail(402, echo="该团队已存在")
    if TeamModel().api_insert_uidAndName(uid, name):
        return Ret.success()
    else:
        return Ret.fail(500, echo="创建团队失败")


@Controller.post('list')
async def list():
    uid = Input.Header.Int("uid")
    team_list = TeamModel().api_select_byUid(uid)
    if team_list:
        return Ret.success(data=team_list)
    else:
        return Ret.success(echo="没有团队")


@Controller.post('delete')
async def delete():
    uid = Input.Header.Int("uid")
    id = Input.Post.Int("id")
    if TeamModel().api_delete_byUidAndTeamId(uid, id):
        return Ret.success()
    else:
        return Ret.fail(500, echo="删除团队失败")


@Controller.post('update')
async def update():
    uid = Input.Header.Int("uid")
    id = Input.Post.Int("id")
    name = Input.Post.Str("name")
    img = Input.Post.Str("img")
    content = Input.Post.Str("content")
    prefix = Input.Post.Str("prefix")
    if TeamModel().api_update_byUidAndId(uid, id, name, img, content, prefix):
        return Ret.success()
    else:
        return Ret.fail(500, echo="更新团队失败")
