import os

from flask import Blueprint

from app.v1.team.model.TeamModel import TeamModel
from app.v1.team.model.TeamSubtokenModel import TeamSubtokenModel
from app.v1.user.model.UserTeamModel import UserTeamModel
from common.controller.LoginController import LoginedController
from tuuz.Calc import Token, Encrypt
from tuuz.Input import Header, Post
from tuuz.Ret import fail, success

Controller = Blueprint(os.path.splitext(os.path.basename(__file__))[0], __name__)


@Controller.before_request
def before():
    return LoginedController()


@Controller.post('/')
def slash():
    return Controller.name


@Controller.post('create')
async def create():
    uid = Header.Int("uid")
    team_id = Post.Int("team_id")
    prefix = Post.Str("prefix")
    amount = Post.Float("amount")
    team = TeamModel().api_find_byId(team_id)
    if not team:
        return fail(404, echo="没有找到对应团队")
    ut = UserTeamModel().api_find_byUidAndTeamId_inRole(uid, team_id, "owner,admin")
    if not ut:
        return fail(403, echo="仅支持团队管理员操作")
    key = Encrypt.sha256(Token.generate_order_id())
    is_limit = True
    if amount < 0:
        is_limit = False
    if TeamSubtokenModel().api_insert(team_id, prefix, key, is_limit, amount):
        return success(data={
            "key": key,
            "prefix": prefix,
        })
    else:
        return fail(500, echo="创建失败")


@Controller.post('list')
async def list():
    uid = Header.Int("uid")
    teamids = UserTeamModel().api_column_teamId_byUid(uid)
    if not teamids:
        return success(echo="还未加入团队")
    team_list = TeamSubtokenModel().api_select_inTeamId(teamids)
    if team_list:
        return success(data=team_list)
    else:
        return success(echo="还未创建token")


@Controller.post('delete')
async def delete():
    id = Post.Int("id")
    team_id = Post.Int("team_id")
    ut = UserTeamModel().api_find_byUidAndTeamId_inRole(uid, team_id, "owner,admin")
    if not ut:
        return fail(403, echo="仅支持团队管理员操作")
    if TeamSubtokenModel().api_delete(team_id, id):
        return success()
    else:
        return fail(500, echo="删除失败")


@Controller.post('get')
async def get():
    uid = Header.Int("uid")
    id = Post.Int("id")
    team_id = Post.Int("team_id")
    if UserTeamModel().api_find_byUidAndTeamId(uid, team_id) is None:
        return fail(403, echo="你不在这个团队中")
    data = TeamSubtokenModel().api_find_byIdAndTeamId(id, team_id)
    if not data:
        return fail(404, echo="没有找到对应的token")
    return success(data=data)
