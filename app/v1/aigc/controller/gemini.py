from flask import Blueprint
from gemini_webapi import GeminiClient, ChatSession

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
    global client, chat,gemini
    token = tuuz.Input.Get.String("token")
    text = tuuz.Input.Get.String("text")
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
                gemini = tuuz.Database.Db().table("ai_gemini").whereRow('project_name', data["name"]).find()
                client=None
                return tuuz.Ret.fail(400, e)
    if gemini["cid"] is None or gemini["rid"] is None or gemini["rcid"] is None:
        chat=client.start_chat()
    chat =ChatSession(client, cid=gemini["cid"], rid=gemini["rid"], rcid=gemini["rcid"])
    response = await chat.send_message(text)
    tuuz.Database.Db().table("ai_gemini").whereRow('project_name', data["name"]).update({"rcid": chat.rcid, "cid": chat.cid, "rid": chat.rid})
    print(response)
    return tuuz.Ret.fail(400, response)
