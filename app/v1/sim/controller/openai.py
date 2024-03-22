
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
    token = tuuz.Input.Combi.String("token")
    data = tuuz.Database.Db().table("ai_project").whereRow('token', token).find()
    if data is None:
        return tuuz.Ret.fail(400, 'project未启用')
    pass


bot = None

cont = 0


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
        if bing["conversation"] is not None or "":
            conversation = json.loads(bing["conversation"])
            await bot.chat_hub.set_conversation(conversation_dict=conversation)
            print("设定conversation")
    except Exception as error:
        if bot is not None:
            await bot.close()
        bot = None
        print("error-conversation", error)
        return tuuz.Ret.fail(500, error, "conversation设定故障")
    try:
        response = await bot.ask(
            prompt=text,
            conversation_style=ConversationStyle.precise,
            simplify_response=False,
        )
    except Exception as error:
        if bot is not None:
            await bot.close()
        bot = None
        print("error-bot-ask", error)
        global cont
        cont += 1
        if cont > 1:
            cont = 0
            return tuuz.Ret.fail(500, error, "生成失败，请重新提问")
        else:
            return text()

    # If you are using non ascii char you need set ensure_ascii=False
    print("response:", json.dumps(response, indent=2, ensure_ascii=False))
    conversation = await bot.chat_hub.get_conversation()
    # print(conversation)
    tuuz.Database.Db().table("ai_bing").whereRow('project_name', data["name"]).update({"conversation": json.dumps(conversation)})
    if response["item"]["throttling"]["numUserMessagesInConversation"] >= response["item"]["throttling"]["maxNumUserMessagesInConversation"]:
        if bot is not None:
            await bot.close()
        bot = None
    messages = response["item"]["messages"]
    output_cleaned = re.sub(r'\[\^\d\^]', '', response["item"]["result"]["message"])
    final_resp = output_cleaned.replace("<br>", "\n")
    normal_text = final_resp
    normal_text_length = len(normal_text)
    for item in messages:
        if "sourceAttributions" in item:
            if len(item['sourceAttributions']) > 0:
                final_resp += "\n\n另外查到一些数据供你参考：\n"
                for sourceAttributions in item['sourceAttributions']:
                    if "providerDisplayName" in sourceAttributions and "seeMoreUrl" in sourceAttributions:
                        title = sourceAttributions['providerDisplayName']
                        if normal_text_length < 100:
                            normal_text += ";" + truncate_text(title, 100)
                        title = truncate_text(title, 20)
                        url = sourceAttributions['seeMoreUrl']
                        final_resp += "\n" + f"{title}:\n{url}\n"
                        print(f"标题：{title}\nURL：{url}\n")
    final_resp = re.sub(r'\n', r'\r\n', final_resp)
    endtime = time.time()
    print("运行时间", endtime - starttime)
    try:
        tuuz.Database.Db().table("log").insert({"project": data["name"], "ask": text, "reply": json.dumps(response, indent=2, ensure_ascii=False)})
    except Exception as error:
        print("db-log", error)
    return tuuz.Ret.success(0, normal_text, final_resp)
