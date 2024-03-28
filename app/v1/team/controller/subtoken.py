import os

from flask import Blueprint

from app.v1.coin.model.CoinModel import CoinModel
from app.v1.team.model.TeamSubtokenModel import TeamSubtokenModel
from app.v1.user.model.UserTeamModel import UserTeamModel
from common.controller.LoginController import LoginedController
from tuuz.Input import Header, Post
from tuuz.Ret import fail, success

Controller = Blueprint(os.path.splitext(os.path.basename(__file__))[0], __name__)


@Controller.before_request
def before():
    LoginedController()
    uid = Header.Int("uid")
    team_id = Post.Int("team_id")
    ut = UserTeamModel().api_find_byUidAndTeamId(uid, team_id)
    if not ut:
        return fail(404, echo="你不在这个团队")
    if ut["role"] != "owner" and ut["role"] != "admin":
        return fail(403, echo="没有权限")


@Controller.post('/')
def slash():
    return "/"


@Controller.post('create')
async def create():
    team_id = Post.Int("team _id")
    coin_id = Post.Int("coin_id")
    prefix = Post.Str("prefix")
    amount = Post.Float("amount")
    coin = CoinModel().api_find(coin_id)
    if not coin:
        return fail(404, echo="没有找到币")
    if TeamSubtokenModel().api_insert(team_id, coin_id, prefix, amount):
        return success()
    else:
        return fail(500, echo="创建失败")


@Controller.post('list')
async def list():
    team_id = Post.Int("team_id")
    team_list = TeamSubtokenModel().api_select_byTeamId(team_id)
    if team_list:
        return success(data=team_list)
    else:
        return success(echo="还未创建团队")


@Controller.post('delete')
async def delete():
    id = Post.Int("id")
    team_id = Post.Int("team_id")
    if TeamSubtokenModel().api_delete(team_id, id):
        return success()
    else:
        return fail(500, echo="删除失败")
