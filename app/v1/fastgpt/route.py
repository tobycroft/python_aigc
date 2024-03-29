import os

from flask import Blueprint

script_path = os.path.abspath(__file__)
folder_path = os.path.dirname(script_path)
folder_name = os.path.basename(folder_path)
Route = Blueprint(folder_name, __name__)


@Route.route("/")
def index():
    return folder_name


# info
import app.v1.fastgpt.controller.direct as info

Route.register_blueprint(info.Controller, url_prefix=info.Controller.name)

# embed
import app.v1.fastgpt.controller.embed as embed

Route.register_blueprint(embed.Controller, url_prefix=embed.Controller.name)

# api
import app.v1.fastgpt.controller.api as api

Route.register_blueprint(api.Controller, url_prefix=api.Controller.name)
