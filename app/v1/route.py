import os

from flask import Blueprint

script_path = os.path.abspath(__file__)
folder_path = os.path.dirname(script_path)
folder_name = os.path.basename(folder_path)

Route = Blueprint('Route', __name__)


@Route.route("/")
def index():
    return folder_name


import app.v1.aigc.route as aigc

Route.register_blueprint(aigc.Route, url_prefix=aigc.folder_name)

import app.v1.llm.route as llm

Route.register_blueprint(llm.Route, url_prefix=llm.folder_name)

import app.v1.tts.route as tts

Route.register_blueprint(tts.Route, url_prefix=tts.folder_name)

import app.v1.langchain.route as langchain

Route.register_blueprint(langchain.Route, url_prefix=langchain.folder_name)
