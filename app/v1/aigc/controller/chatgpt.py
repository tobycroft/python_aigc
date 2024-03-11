import os

from flask import Blueprint
from re_gpt import SyncChatGPT

import tuuz.Database
import tuuz.Input
import tuuz.Ret

ChatGptController = Blueprint(os.path.splitext(os.path.basename(__file__))[0], __name__)


@ChatGptController.route('/')
def slash():
    return "/"


@ChatGptController.before_request
def before():
    token = tuuz.Input.Get.String("token")
    data = tuuz.Database.Db().table("ai_project").whereRow('token', token).find()
    if data is None:
        return tuuz.Ret.fail(400, 'project未启用')
    pass


@ChatGptController.post('/text')
async def text():
    token = tuuz.Input.Get.String("token")
    text = tuuz.Input.Post.String("text")
    data = tuuz.Database.Db().table("ai_project").whereRow('token', token).find()
    bing = tuuz.Database.Db().table("ai_chatgpt").whereRow('project_name', data["name"]).find()
    if bing["cookies"] is None:
        return tuuz.Ret.fail(400, 'bing未启用')
    with SyncChatGPT(session_token=bing["session"]) as chatgpt:
        if bing["conversation"] is None:
            conversation = chatgpt.create_new_conversation()
        else:
            conversation = chatgpt.get_conversation(bing["conversation"])
    msgs = conversation.chat(text)
    for message in msgs:
        print(message["content"], flush=True, end="")
    return tuuz.Ret.success(0, msgs)
