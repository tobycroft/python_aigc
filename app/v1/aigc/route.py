import os

from flask import Blueprint

script_path = os.path.abspath(__file__)
folder_path = os.path.dirname(script_path)
folder_name = os.path.basename(folder_path)
Route = Blueprint(folder_name, __name__)


@Route.route("/")
def index():
    return folder_name


import app.v1.aigc.controller.gemini

Route.register_blueprint(app.v1.aigc.controller.gemini.Controller, url_prefix="/gemini")

import app.v1.aigc.controller.bing

Route.register_blueprint(app.v1.aigc.controller.bing.Controller, url_prefix="/bing")

import app.v1.aigc.controller.chatgpt

Route.register_blueprint(app.v1.aigc.controller.chatgpt.Controller, url_prefix="/chatgpt")

import app.v1.aigc.controller.groq

Route.register_blueprint(app.v1.aigc.controller.groq.Controller, url_prefix="/groq")
