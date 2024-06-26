import os

from flask import Blueprint
from gemini_webapi import GeminiClient, ChatSession

import tuuz.Database
import tuuz.Input
import tuuz.Ret

Controller = Blueprint(os.path.splitext(os.path.basename(__file__))[0], __name__)


@Controller.route('/')
def slash():
    return "/"


@Controller.before_request
def before():
    token = tuuz.Input.Header.String("token")
    data = tuuz.Database.Db().table("ai_project").where('token', token).find()
    if data is None:
        return tuuz.Ret.fail(400, 'project未启用')
    pass


@Controller.post('/text')
async def text():
    global client, chat, gemini
    token = tuuz.Input.Header.String("token")
    text = tuuz.Input.Post.String("text")
    data = tuuz.Database.Db().table("ai_project").where('token', token).find()
    gemini = tuuz.Database.Db().table("ai_gemini").where('project_name', data["name"]).find()
    if gemini is None:
        return tuuz.Ret.fail(400, 'gemini未启用')
    client = GeminiClient(gemini["Secure_1PSID"], gemini["Secure_1PSIDTS"], proxy=None)
    try:
        await client.init(timeout=30, auto_close=False, close_delay=300)
    except Exception as e:
        gemini = tuuz.Database.Db().table("ai_gemini").where('project_name', data["name"]).find()
        client = None
        return tuuz.Ret.fail(500, e, e)
    if gemini["cid"] is None or gemini["rid"] is None or gemini["rcid"] is None:
        chat = client.start_chat()
    chat = ChatSession(client, cid=gemini["cid"], rid=gemini["rid"], rcid=gemini["rcid"])
    response = await chat.send_message(text)
    tuuz.Database.Db().table("ai_gemini").where('project_name', data["name"]).update({"rcid": chat.rcid, "cid": chat.cid, "rid": chat.rid})
    tuuz.Database.Db().table("log").insert({"type": "gemini", "project": data["name"], "ask": text, "reply": response.text})
    print(response)
    return tuuz.Ret.success(0, {"text": response.text, "image": response.images}, response.text)


@Controller.post('/test')
async def test():
    data = tuuz.Database.Db().table("log").where("type", "gemini").find()
    if data is None:
        tuuz.Ret.fail(404)
    return tuuz.Ret.success(0, data, data["reply"])
