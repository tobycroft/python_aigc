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

import app.v1.coin.route as coin

Route.register_blueprint(coin.Route, url_prefix=coin.folder_name)

import app.v1.fastgpt.route as fastgpt

Route.register_blueprint(fastgpt.Route, url_prefix=fastgpt.folder_name)

import app.v1.langchain.route as langchain

Route.register_blueprint(langchain.Route, url_prefix=langchain.folder_name)

import app.v1.pack.route as pack

Route.register_blueprint(pack.Route, url_prefix=pack.folder_name)

import app.v1.share.route as share

Route.register_blueprint(share.Route, url_prefix=share.folder_name)

import app.v1.system.route as system

Route.register_blueprint(system.Route, url_prefix=system.folder_name)

import app.v1.team.route as team

Route.register_blueprint(team.Route, url_prefix=team.folder_name)

import app.v1.tts.route as tts

Route.register_blueprint(tts.Route, url_prefix=tts.folder_name)

import app.v1.user.route as user

Route.register_blueprint(user.Route, url_prefix=user.folder_name)
