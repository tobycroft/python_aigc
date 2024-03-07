from flask import Blueprint

import tuuz.Database
import tuuz.Input
import tuuz.Ret

gemini = Blueprint("gemini", __name__)


@gemini.route('/')
def slash():
    return "/"


@gemini.before_app_request
def before():
    token = tuuz.Input.Get.String("token")

    print(tuuz.Database.Db().table("ai_project").whereRow('token', token).buildSql().find())
    print(tuuz.Database.Db().table("ai_project").whereRow('token', token).find())
    pass


@gemini.route('/index')
def index():
    # print(tuuz.Input.Post.String("a"))
    data = tuuz.Database.Db().table("ai_project").find()
    return tuuz.Ret.fail(400, data)
