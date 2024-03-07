import os

from flask import Blueprint

import app.v1.index.controller.index

script_path = os.path.abspath(__file__)
folder_path = os.path.dirname(script_path)
folder_name = os.path.basename(folder_path)
Route = Blueprint('Route', __name__)


@Route.route("/")
def index():
    return folder_name


Route.register_blueprint(app.v1.index.controller.index.Index, url_prefix="/" + folder_name)
