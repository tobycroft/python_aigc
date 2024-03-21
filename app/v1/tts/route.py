import os

from flask import Blueprint

script_path = os.path.abspath(__file__)
folder_path = os.path.dirname(script_path)
folder_name = os.path.basename(folder_path)
Route = Blueprint(folder_name, __name__)


@Route.route("/")
def index():
    return folder_name


import app.v1.tts.controller.stt as stt

Route.register_blueprint(stt.Controller, url_prefix=stt.Controller.name)

import app.v1.tts.controller.tts as tts

Route.register_blueprint(tts.Controller, url_prefix=tts.Controller.name)
