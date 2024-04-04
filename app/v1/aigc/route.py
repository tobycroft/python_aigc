import os

from flask import Blueprint

script_path = os.path.abspath(__file__)
folder_path = os.path.dirname(script_path)
folder_name = os.path.basename(folder_path)
Route = Blueprint(folder_name, __name__)


@Route.route("/")
def index():
    return folder_name


import app.v1.aigc.controller.gemini as gemini

Route.register_blueprint(gemini.Controller, url_prefix=gemini.Controller.name)

import app.v1.aigc.controller.bing as bing

Route.register_blueprint(bing.Controller, url_prefix=bing.Controller.name)

import app.v1.aigc.controller.chatgpt as chatgpt

Route.register_blueprint(chatgpt.Controller, url_prefix=chatgpt.Controller.name)

import app.v1.aigc.controller.groq as groq

Route.register_blueprint(groq.Controller, url_prefix=groq.Controller.name)

import app.v1.aigc.controller.qwen as qwen

Route.register_blueprint(qwen.Controller, url_prefix=qwen.Controller.name)
