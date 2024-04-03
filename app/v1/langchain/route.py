import os

from flask import Blueprint

script_path = os.path.abspath(__file__)
folder_path = os.path.dirname(script_path)
folder_name = os.path.basename(folder_path)
Route = Blueprint(folder_name, __name__)


@Route.route("/")
def index():
    return folder_name


import app.v1.langchain.controller.milvus as milvus

Route.register_blueprint(milvus.Controller, url_prefix=milvus.Controller.name)

import app.v1.langchain.controller.fastgpt as openai

Route.register_blueprint(openai.Controller, url_prefix=openai.Controller.name)
