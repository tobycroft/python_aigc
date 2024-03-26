import os

from flask import Blueprint

from common.controller.LoginController import LoginedController
from tuuz import Ret

Controller = Blueprint(os.path.splitext(os.path.basename(__file__))[0], __name__)


@Controller.post('/')
def slash():
    return "/"


@Controller.before_request
def before_request():
    return LoginedController()


@Controller.post('text')
def text():
    Ret.success(0, 'success')
