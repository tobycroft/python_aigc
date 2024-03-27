import os

from flask import Blueprint

from common.controller.LoginController import LoginedController
from tuuz import Ret

Controller = Blueprint(os.path.splitext(os.path.basename(__file__))[0], __name__)


@Controller.before_request
def before():
    return LoginedController()


@Controller.post('/')
def slash():
    return "/"


@Controller.post('create')
async def create():
    pass
    return Ret.success(0)
