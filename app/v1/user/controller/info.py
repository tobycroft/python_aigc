import os

from flask import Blueprint

import Ret
from tuuz import Redis
from Redis import String

Controller = Blueprint(os.path.splitext(os.path.basename(__file__))[0], __name__)


@Controller.before_request
def before():
    pass


@Controller.post('/')
def slash():
    return "/"


@Controller.post('index')
async def index():
    String.string_set('key', 'value')
    return Ret.success(0)
