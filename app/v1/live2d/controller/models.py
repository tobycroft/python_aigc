import os

from flask import Blueprint

from tuuz import Ret

Controller = Blueprint(os.path.splitext(os.path.basename(__file__))[0], __name__)


@Controller.post('/')
def slash():
    return Controller.name


@Controller.post('index')
async def index():
    return Ret.success(0)
