import os

from flask import Blueprint

from tuuz import Ret, Database
from tuuz.Redis import String

Controller = Blueprint(os.path.splitext(os.path.basename(__file__))[0], __name__)


@Controller.before_request
def before():
    pass


@Controller.post('/')
def slash():
    return Controller.name


@Controller.post('index')
async def index():
    return Ret.success(0)
