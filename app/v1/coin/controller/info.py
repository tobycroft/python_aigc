import os

from flask import Blueprint

from app.v1.coin.model.CoinModel import CoinModel
from common.controller.LoginController import LoginedController
from tuuz import Ret

Controller = Blueprint(os.path.splitext(os.path.basename(__file__))[0], __name__)


@Controller.before_request
def before():
    return LoginedController()


@Controller.post('/')
def slash():
    return Controller.name


@Controller.post('list')
async def list():
    data = CoinModel().api_select()
    return Ret.success(data=data)
