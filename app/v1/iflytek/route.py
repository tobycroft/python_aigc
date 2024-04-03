import os

from flask import Blueprint

script_path = os.path.abspath(__file__)
folder_path = os.path.dirname(script_path)
folder_name = os.path.basename(folder_path)
Route = Blueprint(folder_name, __name__)


@Route.route("/")
def index():
    return folder_name


# tts
import app.v1.iflytek.controller.tts as tts

Route.register_blueprint(tts.Controller, url_prefix=tts.Controller.name)

# info
import app.v1.iflytek.controller.info as info

Route.register_blueprint(info.Controller, url_prefix=info.Controller.name)
