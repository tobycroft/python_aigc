import os

from sanic import Blueprint

script_path = os.path.abspath(__file__)
folder_path = os.path.dirname(script_path)
folder_name = os.path.basename(folder_path)

v1 = Blueprint(folder_name, url_prefix="/v1")


@v1.route("/")
def v1_root(c):
    return folder_name

#
# # aigc
# import app.v1.aigc.route as aigc
#
# v1.register_blueprint(aigc.Route, url_prefix=aigc.folder_name)
#
# # coin
# import app.v1.coin.route as coin
#
# v1.register_blueprint(coin.Route, url_prefix=coin.folder_name)
#
# # fastgpt
# import app.v1.fastgpt.route as fastgpt
#
# v1.register_blueprint(fastgpt.Route, url_prefix=fastgpt.folder_name)
#
# # iflytek
# import app.v1.iflytek.route as iflytek
#
# v1.register_blueprint(iflytek.Route, url_prefix=iflytek.folder_name)
#
# # knowledge
# import app.v1.knowledge.route as knowledge
#
# v1.register_blueprint(knowledge.Route, url_prefix=knowledge.folder_name)
#
# # langchain
# import app.v1.langchain.route as langchain
#
# v1.register_blueprint(langchain.Route, url_prefix=langchain.folder_name)
#
# # notification
# import app.v1.notification.route as notification
#
# v1.register_blueprint(notification.Route, url_prefix=notification.folder_name)
#
# # pack
# import app.v1.pack.route as pack
#
# v1.register_blueprint(pack.Route, url_prefix=pack.folder_name)
#
# # share
# import app.v1.share.route as share
#
# v1.register_blueprint(share.Route, url_prefix=share.folder_name)
#
# # system
# import app.v1.system.route as system
#
# v1.register_blueprint(system.Route, url_prefix=system.folder_name)
#
# # team
# import app.v1.team.route as team
#
# v1.register_blueprint(team.Route, url_prefix=team.folder_name)
#
# # tts
# import app.v1.tts.route as tts
#
# v1.register_blueprint(tts.Route, url_prefix=tts.folder_name)
#
# # user
# import app.v1.user.route as user
#
# v1.register_blueprint(user.Route, url_prefix=user.folder_name)
#
# # vrm
# import app.v1.vrm.route as vrm
#
# v1.register_blueprint(vrm.Route, url_prefix=vrm.folder_name)
