import os

from flask import Blueprint

from app.v1.coin.model.CoinModel import CoinModel
from app.v1.fastgpt.model.FastgptModel import FastgptModel
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
    return Controller.name


@Controller.post('create')
async def create():
    uid = Header.Int("uid")
    team_id = Post.Int("team_id")
    from_id = Post.Int("from_id")
    coin_id = Post.Int("coin_id")
    prefix = Post.Str("prefix")
    amount = Post.Float("amount")
    team = TeamModel().api_find_byId(team_id)
    if not team:
        return fail(404, echo="没有找到对应团队")
    coin = CoinModel().api_find(coin_id)
    if not coin:
        return fail(404, echo="没有找到对应模型")
    if coin["id"] == 5:
        if not FastgptModel().api_find_byId(from_id):
            return fail(404, echo="上级的Key未找到，请先配置上级的Key")

    key = Encrypt.sha256(Token.generate_order_id())
    is_limit = True
    if amount < 0:
        is_limit = False
    if TeamSubtokenModel().api_insert(uid, team_id, coin_id, from_id, prefix, key, is_limit, amount):
        return success(data={
            "key": key,
            "prefix": prefix,
            "coin_name": coin["name"],
            "coin_id": coin_id,
        })
    else:
        return fail(500, echo="创建失败")


@Controller.post('list')
async def list():
    team_list = TeamSubtokenModel()
    if team_list:
        return success(data=team_list)
    else:
        return success(echo="还未创建token")


@Controller.post('delete')
async def delete():
    id = Post.Int("id")
    team_id = Post.Int("team_id")
    if TeamSubtokenModel().api_delete(team_id, id):
        return success()
    else:
        return fail(500, echo="删除失败")


@Controller.post('get')
async def get():
    id = Post.Int("id")
    team_id = Post.Int("team_id")
    data = TeamSubtokenModel().api_find_byIdAndTeamId(id, team_id)
    if not data:
        return fail(404, echo="没有找到对应的token")
    return success(data=data)
