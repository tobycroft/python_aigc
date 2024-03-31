import os

from flask import Blueprint

from app.v1.live2d.model.Live2dModelModel import Live2dModelModel
from tuuz import Ret
from tuuz.Ret import success

Controller = Blueprint(os.path.splitext(os.path.basename(__file__))[0], __name__)


@Controller.post('/')
def slash():
    return Controller.name


@Controller.post('index')
async def index():
    return Ret.success(0)


# list
@Controller.post('list')
async def list():
    datas = Live2dModelModel().api_select()
    success(data=datas)
