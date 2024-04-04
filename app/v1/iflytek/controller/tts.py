import os

from flask import Blueprint, Response

from app.v1.iflytek.action.TtsAction import TtsAction
from app.v1.iflytek.model.IflytekModel import IflytekModel
from app.v1.team.model.TeamSubtokenModel import TeamSubtokenModel
from app.v1.user.model.UserTeamModel import UserTeamModel
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


@Controller.post('audio')
async def audio():
    uid = Header.Int("uid")
    message = Post.Str("message")
    subtoken = Post.Str("subtoken")
    if not subtoken:
        team_id = UserTeamModel().api_column_teamId_byUid(uid)
        if not team_id:
            return Ret.fail(404, echo="你还未加入任何团队")
    else:
        team_id = TeamSubtokenModel().api_value_teamId_bySubtoken(subtoken)
        if not team_id:
            return Ret.fail(404, echo="你还未加入任何团队")
    iflytts = IflytekModel().api_find_inTeamId([team_id])
    if not iflytts:
        return Ret.fail(404, echo="没有找到对应的key")
    b64 = TtsAction(iflytts["app_id"], iflytts["api_key"], iflytts["api_secret"], message, iflytts["vcn"]).data().get_audioBytes()
    return Response(b64, mimetype="audio/mp3")


@Controller.post('auto')
async def auto():
    uid = Header.Int("uid")
    message = Post.Str("message")
    subtoken = Post.Str("subtoken")
    if not subtoken:
        team_id = UserTeamModel().api_column_teamId_byUid(uid)
        if not team_id:
            return Ret.fail(404, echo="你还未加入任何团队")
    else:
        team_id = TeamSubtokenModel().api_value_teamId_bySubtoken(subtoken)
        if not team_id:
            return Ret.fail(404, echo="你还未加入任何团队")

    iflytts = IflytekModel().api_find_inTeamId([team_id])
    if not iflytts:
        return Ret.fail(404, echo="没有找到对应的key")
    b64 = TtsAction(iflytts["app_id"], iflytts["api_key"], iflytts["api_secret"], message, iflytts["vcn"]).data().get_audioBytes()
    return Response(b64, mimetype="audio/mp3")
