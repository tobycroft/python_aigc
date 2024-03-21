import os

from flask import Blueprint

import Input
import tuuz.Ret
from app.v1.langchain.model import QianwenModel

Controller = Blueprint(os.path.splitext(os.path.basename(__file__))[0], __name__)
# file_name, _ = os.path.splitext(os.path.basename(os.path.abspath(__file__)))


@Controller.post('/')
def slash():
    return "/"


@Controller.post('/text')
async def text():
    print(Controller.name)
    token = Input.Post.String("token")
    if QianwenModel.Api_find_byProjectName(token) is None:
        return tuuz.Ret.fail(404, "没有找到对应的项目")
    return tuuz.Ret.success(0, )
