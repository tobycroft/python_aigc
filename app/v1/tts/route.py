import os

from flask import Blueprint

script_path = os.path.abspath(__file__)
folder_path = os.path.dirname(script_path)
folder_name = os.path.basename(folder_path)
Route = Blueprint(folder_name, __name__)


@Route.route("/")
def index():
    return folder_name


import app.v1.tts.controller.index

Route.register_blueprint(app.v1.tts.controller.index.Controller, url_prefix="/tts")

import app.v1.tts.controller.stt

Route.register_blueprint(app.v1.tts.controller.stt.Controller, url_prefix="/stt")
