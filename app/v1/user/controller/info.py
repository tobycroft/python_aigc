import os

from flask import Blueprint

from app.v1.user.model.UserInfoModel import UserInfoModel
from common.controller.LoginController import LoginedController
from tuuz import Ret
from tuuz.Input import Header

Controller = Blueprint(os.path.splitext(os.path.basename(__file__))[0], __name__)


@Controller.before_request
def before():
    return LoginedController()


@Controller.post('/')
def slash():
    return Controller.name


@Controller.post('get')
async def get():
    uid = Header.Int("uid")
    ui = UserInfoModel().api_find_byUid(uid)
    if ui is None:
        UserInfoModel().api_insert(uid, "", "")
        ui = UserInfoModel().api_find_byUid(uid)
    return Ret.success(0, ui)
