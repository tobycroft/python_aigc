import os

from flask import Blueprint

import tuuz.Database
import tuuz.Input
import tuuz.Ret
from extend.groqccoli import Client

Controller = Blueprint(os.path.splitext(os.path.basename(__file__))[0], __name__)


@Controller.route('/')
def slash():
    return "/"


@Controller.before_request
def before():
    token = tuuz.Input.Header.String("token")
    data = tuuz.Database.Db().table("ai_project").whereRow('token', token).find()
    if data is None:
        return tuuz.Ret.fail(400, 'project未启用')
    pass


@Controller.post('/text')
async def text():
    groq_client = Client()
    chat = groq_client.create_chat("人生的意义是什么?")
    print(chat.content)
    return tuuz.Ret.success(0, chat, chat.content)
