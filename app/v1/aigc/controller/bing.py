import json

from flask import Blueprint
from re_edge_gpt import Chatbot, ConversationStyle

import tuuz.Database
import tuuz.Input
import tuuz.Ret

BingController = Blueprint("bing", __name__)


@BingController.route('/')
def slash():
    return "/"


@BingController.before_request
def before():
    token = tuuz.Input.Get.String("token")
    data = tuuz.Database.Db().table("ai_project").whereRow('token', token).find()
    if data is None:
        return tuuz.Ret.fail(400, 'project未启用')
    pass


@BingController.post('/text')
async def text():
    token = tuuz.Input.Get.String("token")
    text = tuuz.Input.Post.String("text")
    data = tuuz.Database.Db().table("ai_project").whereRow('token', token).find()
    bing = tuuz.Database.Db().table("ai_bing").whereRow('project_name', data["name"]).find()
    if bing["cookies"] is None:
        return tuuz.Ret.fail(400, 'bing未启用')
    bot = None
    try:
        cookies = json.loads(bing["cookies"])
        bot = await Chatbot.create(cookies=cookies)
        try:
            global conversation
            conversation = json.loads(bing["conversation"])
            print("设定conversation", conversation)
            await bot.chat_hub.set_conversation(conversation_dict=conversation)
        except:
            conversation = {}
        response = await bot.ask(
            prompt=text,
            conversation_style=ConversationStyle.precise,
            simplify_response=True
        )
        # If you are using non ascii char you need set ensure_ascii=False
        print(json.dumps(response, indent=2, ensure_ascii=False))
        conversation = await bot.chat_hub.get_conversation()
        print(conversation)
        conversation = await bot.chat_hub.get_conversation()
        print(conversation)
        tuuz.Database.Db().table("ai_bing").whereRow('project_name', data["name"]).update({"conversation": json.dumps(conversation)})
        return tuuz.Ret.success(0, response, response["text"])
    except Exception as error:
        raise error
    finally:
        if bot is not None:
            await bot.close()
