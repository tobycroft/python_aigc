import os

from flask import Blueprint
from pymilvus import connections

from tuuz.Ret import success
from tuuz.input.post import Post

Controller = Blueprint(os.path.splitext(os.path.basename(__file__))[0], __name__)


@Controller.post('/')
def slash():
    return Controller.name


@Controller.post('index')
async def index():
    text = Post.Str("text")
    connections.connect(alias="default", host="10.0.0.174", port="19530")
    return success()
