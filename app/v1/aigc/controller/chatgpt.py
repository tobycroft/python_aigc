import os

from flask import Blueprint
from re_gpt import SyncChatGPT

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
    token = tuuz.Input.Header.String("token")
    text = tuuz.Input.Post.String("text")
    data = tuuz.Database.Db().table("ai_project").where('token', token).find()
    bing = tuuz.Database.Db().table("ai_chatgpt").where('project_name', data["name"]).find()
    if bing["session"] is None:
        return tuuz.Ret.fail(400, 'bing未启用')
    with SyncChatGPT(session_token=bing["session"]) as chatgpt:
        if bing["conversation"] is None:
            conversation = chatgpt.create_new_conversation()
            print("new_conv", conversation.conversation_id)
        else:
            conversation = chatgpt.get_conversation(bing["conversation"])
            print("old_conv", conversation.conversation_id)
    tuuz.Database.Db().table("ai_chatgpt").where('project_name', data["name"]).update({"conversation": conversation.conversation_id})
    msgs = conversation.chat(text)
    print(msgs)
    return tuuz.Ret.success(0, msgs)
