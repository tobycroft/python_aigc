import os

from flask import Blueprint

from app.v1.team.model.TeamModel import TeamModel
from app.v1.team.model.TeamSubtokenModel import TeamSubtokenModel
from common.controller.LoginController import LoginedController
from tuuz import Ret
from tuuz.Input import Header, Post

Controller = Blueprint(os.path.splitext(os.path.basename(__file__))[0], __name__)


@Controller.before_request
def before():
    return LoginedController()


@Controller.post('/')
def slash():
    return "/"


@Controller.post('create')
async def create():
    uid = Header.Int("uid")
    team_id = Post.Int("team_id")
    coin_id = Post.Int("coin_id")
    prefix = Post.Str("prefix")
    amount = Post.Float("amount")
    TeamSubtokenModel().api_find_byKey()

@Controller.post('list')
async def list():
    uid = Header.Int("uid")
    team_list = TeamModel().api_select_byUid(uid)
    if team_list:
        return Ret.success(data=team_list)
    else:
        return Ret.success(echo="没有团队")


@Controller.post('delete')
async def delete():
    uid = Header.Int("uid")
    id = Post.Int("id")
    if TeamModel().api_delete_byUidAndTeamId(uid, id):
        return Ret.success()
    else:
        return Ret.fail(500, echo="删除团队失败")


@Controller.post('update')
async def update():
    uid = Header.Int("uid")
    id = Post.Int("id")
    name = Post.Str("name")
    img = Post.Str("img")
    content = Post.Str("content")
    prefix = Post.Str("prefix")
    if TeamModel().api_update_byUidAndId(uid, id, name, img, content, prefix):
        return Ret.success()
    else:
        return Ret.fail(500, echo="更新团队失败")
