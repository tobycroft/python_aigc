from flask import Blueprint

import tuuz.Database
import tuuz.Input
import tuuz.Ret

gemini = Blueprint("gemini", __name__)


@gemini.route('/')
def slash():
    return "/"


@gemini.before_request
def before():
    token = tuuz.Input.Get.String("token")
    data = tuuz.Database.Db().table("ai_project").whereRow('token', token).find()
    if data is None:
        return tuuz.Ret.fail(400, 'project未启用')
    pass


@gemini.route('/text')
def text():
    token = tuuz.Input.Get.String("token")
    print(tuuz.Database.Db().table("ai_project").whereRow('token', token).insert({"name": "gobotqs"}))
    # data = tuuz.Database.Db().table("ai_project").whereRow('token', token).find()
    # gemini = tuuz.Database.Db().table("ai_gemini").whereRow('project_name', data["name"]).find()
    # if gemini is None:
    #     return tuuz.Ret.fail(400, 'gemini未启用')
    #
    return tuuz.Ret.fail(400, )
