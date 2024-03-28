import os

from flask import Blueprint

from app.v1.team.model.TeamModel import TeamModel
from app.v1.user.model.UserTeamModel import UserTeamModel
from common.controller.LoginController import LoginedController
from tuuz.Input import Header
from tuuz.Ret import success

Controller = Blueprint(os.path.splitext(os.path.basename(__file__))[0], __name__)


@Controller.before_request
def before():
    return LoginedController()


@Controller.post('/')
def slash():
    return "/"


@Controller.post('list')
async def list():
    uid = Header.Int("uid")
    team_list = UserTeamModel().api_select(uid)
    if team_list:
        for i in range(len(team_list)):
            team_list[i]["team_info"] = TeamModel().api_find_byId(team_list[i]["team_id"])
        return success(data=team_list)
    else:
        return success(echo="没有团队")
