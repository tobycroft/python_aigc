import json
import os
import re

from flask import Blueprint
from re_edge_gpt import Chatbot, ConversationStyle

import tuuz.Database
import tuuz.Input
import tuuz.Ret

BingController = Blueprint(os.path.splitext(os.path.basename(__file__))[0], __name__)


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


bot = None


@BingController.post('/text')
async def text():
    token = tuuz.Input.Get.String("token")
    text = tuuz.Input.Post.String("text")
    data = tuuz.Database.Db().table("ai_project").whereRow('token', token).find()
    bing = tuuz.Database.Db().table("ai_bing").whereRow('project_name', data["name"]).find()
    if bing["cookies"] is None:
        return tuuz.Ret.fail(400, 'bing未启用')
    global bot
    if bot is None:
        cookies = json.loads(bing["cookies"])
        bot = await Chatbot.create(cookies=cookies)
    try:
        global conversation
        conversation = json.loads(bing["conversation"])
        print("设定conversation")
        await bot.chat_hub.set_conversation(conversation_dict=conversation)

    except Exception as error:
        conversation = {}
        return tuuz.Ret.fail(500, error, "conversation设定故障")

    response = await bot.ask(
        prompt=text,
        conversation_style=ConversationStyle.precise,
        simplify_response=True,
        search_result=False,
    )
    # If you are using non ascii char you need set ensure_ascii=False
    print(json.dumps(response, indent=2, ensure_ascii=False))
    conversation = await bot.chat_hub.get_conversation()
    # print(conversation)
    tuuz.Database.Db().table("ai_bing").whereRow('project_name', data["name"]).update({"conversation": json.dumps(conversation)})
    if response["messages_left"] < 1:
        await bot.close()
        bot = None
    json_str = re.search(r'{.*}', response["text"], re.DOTALL).group()
    result = json.loads(json_str)
    final_resp = ""

    # 去除原始内容中的JSON部分
    output_without_json = re.sub(r'{.*}', '', response["text"], flags=re.DOTALL)
    final_resp += output_without_json

    for item in result['web_search_results']:
        title = item['title']
        url = item['url']
        final_resp += f"标题：{title}\nURL：{url}\n"
        # print(f"标题：{title}\nURL：{url}\n")

    return tuuz.Ret.success(0, response, final_resp)
