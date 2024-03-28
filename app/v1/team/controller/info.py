import os

from flask import Blueprint

from app.v1.team.model import TeamModel
from common.controller.LoginController import LoginedController
from tuuz import Ret, Input

Controller = Blueprint(os.path.splitext(os.path.basename(__file__))[0], __name__)


@Controller.before_request
def before():
    return LoginedController()


@Controller.post('/')
def slash():
    return "/"


@Controller.post('create')
async def create():
    uid = Input.Post.Int("uid")
    name = Input.Post.Str("name")
    TeamModel.api_insert(uid)
    return Ret.success()


@Controller.post('list')
async def list():
    uid = Input.Post.Int("uid")
    team_list = TeamModel.api_select_byUid(uid)
    if team_list:
        return Ret.success(data=team_list)
    else:
        return Ret.success()
