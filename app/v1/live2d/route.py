import os

from flask import Blueprint

script_path = os.path.abspath(__file__)
folder_path = os.path.dirname(script_path)
folder_name = os.path.basename(folder_path)
Route = Blueprint(folder_name, __name__)


@Route.route("/")
def index():
    return folder_name


# models
import app.v1.live2d.controller.models as models

Route.register_blueprint(models.Controller, url_prefix=models.Controller.name)

# tips
import app.v1.live2d.controller.tips as tips

Route.register_blueprint(tips.Controller, url_prefix=tips.Controller.name)
