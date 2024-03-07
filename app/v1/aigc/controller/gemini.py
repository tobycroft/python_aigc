from flask import Blueprint
from gemini_webapi import GeminiClient

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
async def text():
    token = tuuz.Input.Get.String("token")
    data = tuuz.Database.Db().table("ai_project").whereRow('token', token).find()
    gemini = tuuz.Database.Db().table("ai_gemini").whereRow('project_name', data["name"]).find()
    if gemini is None:
        return tuuz.Ret.fail(400, 'gemini未启用')

    client = GeminiClient(gemini["Secure_1PSID"], gemini["Secure_1PSIDTS"], proxy=None)
    await client.init(timeout=30, auto_close=False, close_delay=300)
    chat = client.start_chat()
    response = await chat.send_message("你好?")
    print(response)
    return tuuz.Ret.fail(400, response)
