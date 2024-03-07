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


client = None
chat = None


@gemini.route('/text')
async def text():
    global client, chat
    token = tuuz.Input.Get.String("token")
    data = tuuz.Database.Db().table("ai_project").whereRow('token', token).find()
    gemini = tuuz.Database.Db().table("ai_gemini").whereRow('project_name', data["name"]).find()
    if gemini is None:
        return tuuz.Ret.fail(400, 'gemini未启用')
    if chat is None:
        if client is None:
            client = GeminiClient(gemini["Secure_1PSID"], gemini["Secure_1PSIDTS"], proxy=None)
            try:
                await client.init(timeout=30, auto_close=False, close_delay=300)
            except Exception as e:
                return tuuz.Ret.fail(400, e)
        chat = client.start_chat()
    print(chat.rcid, chat.cid, chat.rid, chat.metadata)
    response = await chat.send_message("你好?")
    print(response.candidates)
    print(chat.rcid, chat.cid, chat.rid, chat.metadata)
    print(response)
    return tuuz.Ret.fail(400, response)
