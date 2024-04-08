import os

from flask import Blueprint

script_path = os.path.abspath(__file__)
folder_path = os.path.dirname(script_path)
folder_name = os.path.basename(folder_path)
Route = Blueprint(folder_name, __name__)

# index
import app.v1.milvus.controller.index as index

Route.register_blueprint(index.Controller, url_prefix=index.Controller.name)
