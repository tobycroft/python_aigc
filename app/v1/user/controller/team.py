import os

from flask import Blueprint

from app.v1.team.model.TeamModel import TeamModel
from app.v1.user.model.UserTeamModel import UserTeamModel
from common.controller.LoginController import LoginedController
from tuuz import Database
from tuuz.Input import Header, Post
from tuuz.Ret import success, fail

Controller = Blueprint(os.path.splitext(os.path.basename(__file__))[0], __name__)


@Controller.before_request
def before():
    return LoginedController()


@Controller.post('/')
def slash():
    return Controller.name


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


@Controller.post('delete')
async def delete():
    uid = Header.Int("uid")
    id = Post.Int("id")
    ut = UserTeamModel().api_find_byUidAndTeamId(uid, id)
    if not ut:
        return fail(404, echo="没有该团队")
    db = Database.Db.connect_to_db()
    db.begin()
    if not UserTeamModel().api_delete_byTeamId(id):
        db.rollback()
        db.close()
        return fail(500, echo="删除团队失败")
    if ut["role"] == "owner" or ut["role"] == "admin":
        if not TeamModel(db).api_delete(id):
            db.rollback()
            db.close()
            return fail(500, echo="删除团队失败")
    db.commit()
    db.close()
    success()
