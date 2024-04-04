import os

from flask import Blueprint, Response

from app.v1.coin.action.CoinCalcAction import CoinCalcAction
from app.v1.iflytek.action.TtsAction import TtsAction
from app.v1.iflytek.model.IflytekModel import IflytekModel
from app.v1.iflytek.model.IflytekRecordModel import IflytekRecordModel
from app.v1.team.model.TeamSubtokenModel import TeamSubtokenModel
from app.v1.user.model.UserTeamModel import UserTeamModel
from common.controller.LoginController import LoginedController
from tuuz import Ret
from tuuz.Input import Header, Post

Controller = Blueprint(os.path.splitext(os.path.basename(__file__))[0], __name__)


@Controller.post('/')
def slash():
    return Controller.name


@Controller.post('auto')
@Controller.post('audio')
async def audio():
    LoginedController()
    uid = Header.Int("uid")
    message = Post.Str("message")
    team_id = UserTeamModel().api_column_teamId_byUid(uid)
    if not team_id:
        return Ret.fail(404, echo="你还未加入任何团队")
    subtokens = TeamSubtokenModel().api_select_byAmountOrIsLimit_inTeamId(team_id, 0, 0)
    if not subtokens:
        return Ret.fail(404, echo="没有找到对应的key")
    key = subtokens[0]["key"]
    iflytts = IflytekModel().api_find_inTeamId([team_id])
    if not iflytts:
        return Ret.fail(404, echo="没有找到对应的key")
    b64 = TtsAction(iflytts["app_id"], iflytts["api_key"], iflytts["api_secret"], message, iflytts["vcn"]).data().get_audioBytes()
    amount = CoinCalcAction("iflytts").Calc(len(message))
    TeamSubtokenModel().api_inc_amount_byKey(key, -abs(amount))
    IflytekRecordModel().api_insert(iflytts["id"], key, message, "", len(message), len(message), len(message), "", amount)
    return Response(b64, mimetype="audio/mp3")


# subtoken
@Controller.post('subtoken')
async def subtoken():
    Authorization = Header.Str("Authorization")
    try:
        auth = Authorization.replace("Bearer ", "").split('-')
        prefix = auth[0]
        key = auth[1]
    except Exception as e:
        return Ret.fail(401, e, echo="Authorization头不正确")
    message = Post.Str("message")
    subtoken = TeamSubtokenModel().api_find_byPrefixAndKey(prefix, key)
    if not subtoken:
        return Ret.fail(404, echo="没有找到对应的key")
    if int(subtoken["is_limit"]) == 1 and float(subtoken["amount"]) <= 0:
        return Ret.fail(403, echo="你的key已经没有余量了，请在控制台增加余量或将key设定为无限量模式")
    iflytts = IflytekModel().api_find_inTeamId([subtoken["team_id"]])
    if not iflytts:
        return Ret.fail(404, echo="没有找到对应的key")
    b64 = TtsAction(iflytts["app_id"], iflytts["api_key"], iflytts["api_secret"], message, iflytts["vcn"]).data().get_audioBytes()
    amount = CoinCalcAction("iflytts").Calc(len(message))
    TeamSubtokenModel().api_inc_amount_byKey(key, -abs(amount))
    IflytekRecordModel().api_insert(iflytts["id"], key, message, "", len(message), len(message), len(message), "", amount)
    return Response(b64, mimetype="audio/mp3")
