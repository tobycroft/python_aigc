import os

from flask import Blueprint

from app.v1.team.model.TeamModel import TeamModel
from app.v1.user.model.UserTeamModel import UserTeamModel
from common.controller.LoginController import LoginedController
from tuuz import Input, Database
from tuuz.Ret import fail, success

Controller = Blueprint(os.path.splitext(os.path.basename(__file__))[0], __name__)


@Controller.before_request
def before():
    return LoginedController()


@Controller.post('/')
def slash():
    return "/"


@Controller.post('create')
async def create():
    uid = Input.Header.Int("uid")
    name = Input.Post.Str("name")
    if len(name) < 1:
        return fail(400, echo="name应该大于1")
    if TeamModel().api_find_byUidAndName(uid, name):
        return fail(402, echo="该团队已存在")

    db = Database.Db.connect_to_db()
    db.begin()
    team_id = TeamModel(db).api_insert_uidAndName(uid, name)
    if team_id:
        if UserTeamModel(db).api_insert(uid, team_id, "owner", ""):
            db.commit()
            return success()
        else:
            db.rollback()
            return fail(500, echo="创建团队失败")
    else:
        db.rollback()
        return fail(500, echo="创建团队失败")


@Controller.post('list')
async def list():
    uid = Input.Header.Int("uid")
    team_list = TeamModel().api_select_byUid(uid)
    if team_list:
        return success(data=team_list)
    else:
        return success(echo="没有团队")


@Controller.post('delete')
async def delete():
    uid = Input.Header.Int("uid")
    id = Input.Post.Int("id")
    ut = UserTeamModel().api_find_byUidAndTeamId(uid, id)
    if not ut:
        return fail(404, echo="没有该团队")
    if ut["role"] != "owner" and ut["role"] != "admin":
        return fail(403, echo="没有权限")
    if TeamModel().api_delete_byUidAndTeamId(uid, id):
        return success()
    else:
        return fail(500, echo="删除团队失败")


@Controller.post('update')
async def update():
    uid = Input.Header.Int("uid")
    id = Input.Post.Int("id")
    name = Input.Post.Str("name")
    img = Input.Post.Str("img")
    content = Input.Post.Str("content")
    prefix = Input.Post.Str("prefix")
    ut = UserTeamModel().api_find_byUidAndTeamId(uid, id)
    if not ut:
        return fail(404, echo="没有该团队")
    if ut["role"] != "owner" and ut["role"] != "admin":
        return fail(403, echo="没有权限")
    if TeamModel().api_update_byUidAndId(uid, id, name, img, content, prefix):
        return success()
    else:
        return fail(500, echo="更新团队失败")
