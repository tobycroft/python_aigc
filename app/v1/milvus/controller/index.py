import os

from flask import Blueprint
from pymilvus import connections
from pymilvus.orm import utility

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

    # has = utility.has_collection("collection_5")
    #
    # print(f"Does collection collection_5 exist in Milvus: {has}")
    return success(0, utility.list_usernames())
