import os

from flask import Blueprint

script_path = os.path.abspath(__file__)
folder_path = os.path.dirname(script_path)
folder_name = os.path.basename(folder_path)
Route = Blueprint(folder_name, __name__)


@Route.route("/")
def index():
    return folder_name


import app.v1.user.controller.auth as auth

Route.register_blueprint(auth.Controller, url_prefix=auth.Controller.name)

import app.v1.user.controller.info as info

Route.register_blueprint(info.Controller, url_prefix=info.Controller.name)

import app.v1.user.controller.team as team

Route.register_blueprint(team.Controller, url_prefix=team.Controller.name)
