import json
import os
from http import HTTPStatus

import dashscope
from dashscope.api_entities.dashscope_response import Message
from flask import Blueprint
from openai import OpenAI

from app.v1.coin.action.CoinCalcAction import CoinCalcAction
from app.v1.qwen.model.QianwenModel import QianwenModel
from app.v1.qwen.model.QianwenRecordModel import QianwenRecordModel
from app.v1.team.model.TeamSubtokenModel import TeamSubtokenModel
from app.v1.user.model.UserTeamModel import UserTeamModel
from common.controller.LoginController import LoginedController
from tuuz import Ret
from tuuz.Input import Header, Post
from tuuz.Ret import success

Controller = Blueprint(os.path.splitext(os.path.basename(__file__))[0], __name__)


@Controller.post('/')
def slash():
    return Controller.name


@Controller.post('text')
def text():
    LoginedController()
    uid = Header.Int("uid")
    chat_id = Post.Str("chat_id")
    message = Post.Str("message")
    teamids = UserTeamModel().api_column_teamId_byUid(uid)
    if not teamids:
        return Ret.fail(404, echo="你还未加入任何团队")
    subtokens = TeamSubtokenModel().api_select_byAmountOrIsLimit_inTeamId(teamids, 0, 0)
    if not subtokens:
        return Ret.fail(404, echo="没有找到可用的key")
    subtoken = subtokens[0]
    team_id = subtoken["team_id"]
    key = subtoken["key"]
    qwen = QianwenModel().api_find_inTeamId([team_id])
    if not qwen:
        return Ret.fail(404, echo="没有找到对应的key")
    messages: list[dict] = []
    records = QianwenRecordModel().api_find_bySubtokenAndChatId(key, chat_id)
    if records:
        messages += json.loads(records["send"])
    messages.append({"role": "user", "content": message})
    client = OpenAI(api_key=qwen["key"], base_url=qwen["base_url"])

    ret = client.chat.completions.create(
        model=qwen["model"],
        messages=messages,
        response_format={"type": "json_object"},
        extra_body={
            "chatId": chat_id,
            "detail": qwen["detail"],
        }
        # temperature=0,
    )
    total_tokens = ret.usage.total_tokens
    prompt_tokens = ret.usage.prompt_tokens
    completion_tokens = ret.usage.completion_tokens

    amount = CoinCalcAction("qwen1.8").Calc(total_tokens)
    TeamSubtokenModel().api_inc_amount_byKey(key, -abs(amount))
    QianwenRecordModel().api_insert(qwen["id"], key, chat_id, json.dumps(messages, ensure_ascii=False), ret.model_dump_json(),
                                    completion_tokens, prompt_tokens, total_tokens, "stop", amount)

    # print(ret.model_dump(), total_tokens, prompt_tokens, completion_tokens)
    ret_message = ""
    if len(ret.choices) > 0:
        ret_message = ret.choices[0].message.content
    return success(data=messages, echo=ret_message)


@Controller.post('raw')
def raw():
    Authorization = Header.Str("Authorization")
    try:
        auth = Authorization.replace("Bearer ", "").split('-')
        prefix = auth[0]
        key = auth[1]
    except Exception as e:
        return Ret.fail(401, e, echo="Authorization头不正确")
    chat_id = Post.Str("chat_id")
    message = Post.Str("message")
    subtoken = TeamSubtokenModel().api_find_byPrefixAndKey(prefix, key)
    if not subtoken:
        return Ret.fail(404, echo="没有找到对应的key")
    team_id = subtoken["team_id"]
    key = subtoken["key"]
    qianwen = QianwenModel().api_find_inTeamId([team_id])
    if not qianwen:
        return Ret.fail(404, echo="没有找到对应的key")
    prompt = qianwen["prompt"]
    messages = list[Message]([
        {"role": "system",
         "content": prompt
         },
    ])
    records = QianwenRecordModel().api_find_bySubtokenAndChatId(key, chat_id)
    if records:
        messages += json.loads(records["reply"])
    messages.append(Message("user", message))

    api_key = qianwen["key"]
    dashscope.api_key = api_key
    response = dashscope.Generation.call(
        model="qwen-1.8b-chat",
        messages=messages,
        # seed=1234,
        top_p=0.83,
        result_format='message',
        max_tokens=1500,
        temperature=0.7,
        repetition_penalty=0.7,
    )
    if response.status_code == HTTPStatus.OK:
        print(response)
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))
    total_tokens = response.usage.total_tokens
    prompt_tokens = response.usage.input_tokens
    completion_tokens = response.usage.output_tokens

    amount = CoinCalcAction("qwen1.8").Calc(total_tokens)
    TeamSubtokenModel().api_inc_amount_byKey(subtoken["key"], -abs(amount))

    QianwenRecordModel().api_insert(qianwen["id"], key, chat_id, json.dumps(messages, ensure_ascii=False), json.dumps(response.output.choices, ensure_ascii=False),
                                    completion_tokens, prompt_tokens, total_tokens, "stop", amount)

    # print(ret.model_dump(), total_tokens, prompt_tokens, completion_tokens)
    ret_message = ""
    if len(response.output.choices) > 0:
        ret_message = response.output.choices[0].message.content
    return success(data=response, echo=ret_message)
