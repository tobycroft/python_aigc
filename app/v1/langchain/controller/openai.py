import os

from flask import Blueprint

from tuuz import Database, Ret

Controller = Blueprint(os.path.splitext(os.path.basename(__file__))[0], __name__)


@Controller.post('/')
def slash():
    return "/"


@Controller.before_request
def before():
    data = Database.Db()
    if data is None:
        return Ret.fail(400, 'project未启用')
    pass
