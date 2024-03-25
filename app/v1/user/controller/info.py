import os

from flask import Blueprint

Controller = Blueprint(os.path.splitext(os.path.basename(__file__))[0], __name__)


@Controller.before_request
def before():
    pass


@Controller.post('/')
def slash():
    return "/"
