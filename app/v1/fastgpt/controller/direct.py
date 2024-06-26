import json
import os

import flask
from flask import Blueprint
from openai import OpenAI

from app.v1.coin.action.CoinCalcAction import CoinCalcAction
from app.v1.fastgpt.model.FastgptModel import FastgptModel
from app.v1.fastgpt.model.FastgptRecordModel import FastgptRecordModel
from app.v1.team.model.TeamSubtokenModel import TeamSubtokenModel
from tuuz import Ret
from tuuz.Input import Header
from tuuz.Ret import json_response

Controller = Blueprint(os.path.splitext(os.path.basename(__file__))[0], __name__)


@Controller.post('/')
def slash():
    return Controller.name


# @Controller.before_request
# def before_request():


@Controller.post('text')
def text():
    Authorization = Header.Str("Authorization")
    try:
        auth = Authorization.replace("Bearer ", "").split('-')
        prefix = auth[0]
        key = auth[1]
    except Exception as e:
        return Ret.fail(401, e, echo="Authorization头不正确")
    subtoken = TeamSubtokenModel().api_find_byPrefixAndKey(prefix, key)
    if not subtoken:
        return Ret.fail(404, echo="没有找到对应的key")
    if int(subtoken["is_limit"]) == 1 and float(subtoken["amount"]) <= 0:
        return Ret.fail(403, echo="你的key已经没有余量了，请在控制台增加余量或将key设定为无限量模式")
    team_id = subtoken["team_id"]
    key = subtoken["key"]
    fastgpt = FastgptModel().api_find_inTeamId([team_id])
    if not fastgpt:
        return Ret.fail(404, echo="没有找到对应的key")
    client = OpenAI(api_key=fastgpt["key"], base_url=fastgpt["base_url"])
    chat_id = flask.request.json.get("chatId")
    messages = flask.request.json.get("messages")
    ret = client.chat.completions.create(
        model=fastgpt["model"],
        messages=messages,
        response_format={"type": "json_object"},
        extra_body={
            "chatId": chat_id,
            "detail": fastgpt["detail"],
        }
        # temperature=0,
    )
    total_tokens = ret.usage.total_tokens
    prompt_tokens = ret.usage.prompt_tokens
    completion_tokens = ret.usage.completion_tokens

    amount = CoinCalcAction("fastgpt").Calc(total_tokens)
    TeamSubtokenModel().api_inc_amount_byKey(key, -abs(amount))

    FastgptRecordModel().api_insert(fastgpt["id"], key, chat_id, json.dumps(messages, ensure_ascii=False), ret.model_dump_json(),
                                    completion_tokens, prompt_tokens, total_tokens, "stop", amount)

    # print(ret.model_dump(), total_tokens, prompt_tokens, completion_tokens)
    return json_response(ret.model_dump())
