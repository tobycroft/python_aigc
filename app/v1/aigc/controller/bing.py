import json
import os
import re
import time

from flask import Blueprint
from re_edge_gpt import Chatbot, ConversationStyle

import tuuz.Database
import tuuz.Input
import tuuz.Ret

Controller = Blueprint(os.path.splitext(os.path.basename(__file__))[0], __name__)


@Controller.route('/')
def slash():
    return "/"


def truncate_text(text, max_length):
    if len(text) > max_length:
        truncated_text = text[:max_length] + "..."
    else:
        truncated_text = text
    return truncated_text


@Controller.before_request
def before():
    token = tuuz.Input.Get.String("token")
    data = tuuz.Database.Db().table("ai_project").whereRow('token', token).find()
    if data is None:
        return tuuz.Ret.fail(400, 'project未启用')
    pass


bot = None


@Controller.post('/text')
async def text():
    token = tuuz.Input.Get.String("token")
    text = tuuz.Input.Post.String("text")
    data = tuuz.Database.Db().table("ai_project").whereRow('token', token).find()
    bing = tuuz.Database.Db().table("ai_bing").whereRow('project_name', data["name"]).find()
    if bing["cookies"] is None:
        return tuuz.Ret.fail(400, 'bing未启用')
    global bot
    starttime = time.time()
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
        bot = None
        print(error)
        return tuuz.Ret.fail(500, error, "conversation设定故障")

    try:
        response = await bot.ask(
            prompt=text,
            conversation_style=ConversationStyle.precise,
            simplify_response=False,
        )
    except Exception as error:
        bot = None
        print(error)
        return tuuz.Ret.fail(500, error, error)

    # If you are using non ascii char you need set ensure_ascii=False
    print(json.dumps(response, indent=2, ensure_ascii=False))
    conversation = await bot.chat_hub.get_conversation()
    # print(conversation)
    tuuz.Database.Db().table("ai_bing").whereRow('project_name', data["name"]).update({"conversation": json.dumps(conversation)})
    # if response["messages_left"] < 1:
    #     await bot.close()
    #     bot = None
    # try:
    messages = response["item"]["messages"]
    output_cleaned = re.sub(r'\[\^\d\^]', '', response["item"]["result"]["message"])
    final_resp = output_cleaned.replace("<br>", "\n")

    for item in messages:
        if "sourceAttributions" in item:
            if len(item['sourceAttributions']) > 0:
                final_resp += "\n\n\n\n另外查到一些数据供你参考：\n"
            for sourceAttributions in item['sourceAttributions']:
                title = sourceAttributions['providerDisplayName']
                max_length = 20
                title = truncate_text(title, max_length)
                url = sourceAttributions['seeMoreUrl']
                final_resp += "\n" + f"{title}:\n{url}\n"
                print(f"标题：{title}\nURL：{url}\n")
    final_resp = re.sub(r'\n', r'\r\n', final_resp)
    #     final_resp = final_resp.replace("Generating answers for you...", "")
    #     final_resp = re.sub(r'Searching the web for.*', '', final_resp)
    # except Exception as e:
    #     final_resp = response["text"]
    endtime = time.time()
    print("运行时间", endtime - starttime)
    return tuuz.Ret.success(0, response, final_resp)


@Controller.post('/stream')
async def stream():
    token = tuuz.Input.Get.String("token")
    text = tuuz.Input.Post.String("text")
    data = tuuz.Database.Db().table("ai_project").whereRow('token', token).find()
    bing = tuuz.Database.Db().table("ai_bing").whereRow('project_name', data["name"]).find()
    if bing["cookies"] is None:
        return tuuz.Ret.fail(400, 'bing未启用')
    global bot
    starttime = time.time()
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
        bot = None
        print(error)
        return tuuz.Ret.fail(500, error, "conversation设定故障")

    try:
        async for final, response in bot.ask_stream(
                prompt=text,
                conversation_style=ConversationStyle.precise,
                search_result=False,
        ):
            print(json.dumps(response, indent=2, ensure_ascii=False))
    except Exception as error:
        bot = None
        print(error)
        return tuuz.Ret.fail(500, error, error)

    endtime = time.time()
    print("运行时间", endtime - starttime)
    return tuuz.Ret.success(0, )
