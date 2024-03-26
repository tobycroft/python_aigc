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
    return "/"


@Controller.post('index')
async def index():
    conn = Database.Db().get_connection()
    print(Database.Db(conn).table("system_param").where("key", "aaaa").update({"value": "cccc"}))
    return Ret.success(0)
