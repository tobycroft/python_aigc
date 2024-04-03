import os

from flask import Blueprint

script_path = os.path.abspath(__file__)
folder_path = os.path.dirname(script_path)
folder_name = os.path.basename(folder_path)

Route = Blueprint('Route', __name__)


@Route.route("/")
def index():
    return folder_name


# aigc
import app.v1.aigc.route as aigc

Route.register_blueprint(aigc.Route, url_prefix=aigc.folder_name)

# coin
import app.v1.coin.route as coin

Route.register_blueprint(coin.Route, url_prefix=coin.folder_name)

# fastgpt
import app.v1.fastgpt.route as fastgpt

Route.register_blueprint(fastgpt.Route, url_prefix=fastgpt.folder_name)

# iflytek
import app.v1.iflytek.route as iflytek

Route.register_blueprint(iflytek.Route, url_prefix=iflytek.folder_name)

# knowledge
import app.v1.knowledge.route as knowledge

Route.register_blueprint(knowledge.Route, url_prefix=knowledge.folder_name)

# langchain
import app.v1.langchain.route as langchain

Route.register_blueprint(langchain.Route, url_prefix=langchain.folder_name)

# notification
import app.v1.notification.route as notification

Route.register_blueprint(notification.Route, url_prefix=notification.folder_name)

# pack
import app.v1.pack.route as pack

Route.register_blueprint(pack.Route, url_prefix=pack.folder_name)

# share
import app.v1.share.route as share

Route.register_blueprint(share.Route, url_prefix=share.folder_name)

# system
import app.v1.system.route as system

Route.register_blueprint(system.Route, url_prefix=system.folder_name)

# team
import app.v1.team.route as team

Route.register_blueprint(team.Route, url_prefix=team.folder_name)

# tts
import app.v1.tts.route as tts

Route.register_blueprint(tts.Route, url_prefix=tts.folder_name)

# user
import app.v1.user.route as user

Route.register_blueprint(user.Route, url_prefix=user.folder_name)

# vrm
import app.v1.vrm.route as vrm

Route.register_blueprint(vrm.Route, url_prefix=vrm.folder_name)

# live2d
import app.v1.live2d.route as live2d

Route.register_blueprint(live2d.Route, url_prefix=live2d.folder_name)

# qwen
import app.v1.qwen.route as qwen

Route.register_blueprint(qwen.Route, url_prefix=qwen.folder_name)
