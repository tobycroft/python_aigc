import os

from flask import Blueprint

from app.v1.fastgpt.model.FastgptModel import FastgptModel
from common.controller.LoginController import LoginedController
from tuuz import Ret
from tuuz.Input import Header

Controller = Blueprint(os.path.splitext(os.path.basename(__file__))[0], __name__)


@Controller.post('/')
def slash():
    return Controller.name


@Controller.before_request
def before_request():
    return LoginedController()


# list
@Controller.post('/list')
def list():
    uid = Header.Int('uid')
    data = FastgptModel().api_select_byUid(uid)
    return Ret.success(data=data)
