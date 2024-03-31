import os

from flask import Blueprint

from app.v1.coin.model.CoinModel import CoinModel
from app.v1.iflytek.action.TtsAction import VmsApi
from app.v1.iflytek.model.IflytekModel import IflytekModel
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
    return Controller.name


@Controller.post('create')
async def text():
    uid = Header.Int("uid")
    subtoken_id = Post.Int("subtoken_id")
    message = Post.Str("message")
    subtoken = TeamSubtokenModel().api_find_byUidAndId(uid, subtoken_id)
    if not subtoken:
        return Ret.fail(404, echo="没有找到对应的key")
    if int(subtoken["is_limit"]) == 1 and float(subtoken["amount"]) <= 0:
        return Ret.fail(403, echo="你的key已经没有余量了，请在控制台增加余量或将key设定为无限量模式")
    if subtoken["coin_id"] != 6:
        coin_name = ""
        coin = CoinModel().api_find(subtoken["coin_id"])
        if coin:
            coin_name = coin["name"]
        return Ret.fail(404, echo="key只能使用于" + coin_name)
    iflytts = IflytekModel().api_find_byId(subtoken["from_id"])
    if not iflytts:
        return Ret.fail(404, echo="讯飞语音中的上级Key被删除")
    vms = VmsApi(iflytts["host"], iflytts["app_id"], iflytts["api_key"], iflytts["api_secret"])
    start_url = "/v1/private/vms2d_start"
    print("启动")
    session = vms.start(start_url)
    if session:
        text_url = "/v1/private/vms2d_ctrl"
        vms.text_ctrl(text_url, session, message)

        stop_url = "/v1/private/vms2d_stop"
        vms.stop(stop_url, session)
        return Ret.success(0)
    else:
        stop_url = "/v1/private/vms2d_stop"
        vms.stop(stop_url, session)
        return Ret.fail(500, echo="讯飞语音创建会话失败")
