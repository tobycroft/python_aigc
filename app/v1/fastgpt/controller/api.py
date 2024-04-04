import json
import os

from flask import Blueprint
from openai import OpenAI

from app.v1.coin.action.CoinCalcAction import CoinCalcAction
from app.v1.fastgpt.model.FastgptModel import FastgptModel
from app.v1.fastgpt.model.FastgptRecordModel import FastgptRecordModel
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


@Controller.before_request
def before_request():
    return LoginedController()


@Controller.post('text')
def text():
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
    fastgpt = FastgptModel().api_find_inTeamId([team_id])
    if not fastgpt:
        return Ret.fail(404, echo="没有找到对应的key")
    messages: list[dict] = []
    records = FastgptRecordModel().api_find_bySubtokenAndChatId(key, chat_id)
    if records:
        messages += json.loads(records["send"])
    messages.append({"role": "user", "content": message})
    client = OpenAI(api_key=fastgpt["key"], base_url=fastgpt["base_url"])

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
    ret_message = ""
    if len(ret.choices) > 0:
        ret_message = ret.choices[0].message.content
    return success(data=messages, echo=ret_message)


@Controller.post('raw')
def raw():
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
    fastgpt = FastgptModel().api_find_inTeamId([team_id])
    if not fastgpt:
        return Ret.fail(404, echo="没有找到对应的key")
    messages: list[dict] = []
    records = FastgptRecordModel().api_find_bySubtokenAndChatId(key, chat_id)
    if records:
        messages += json.loads(records["send"])
    messages.append({"role": "user", "content": message})
    client = OpenAI(api_key=fastgpt["key"], base_url=fastgpt["base_url"])

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

    amount = CoinCalcAction(subtoken["coin_id"]).Calc(total_tokens)
    TeamSubtokenModel().api_inc_amount_byKey(subtoken["key"], -abs(amount))

    FastgptRecordModel().api_insert(fastgpt["id"], subtoken["id"], chat_id, json.dumps(messages, ensure_ascii=False), ret.model_dump_json(),
                                    completion_tokens, prompt_tokens, total_tokens, "stop", amount)

    # print(ret.model_dump(), total_tokens, prompt_tokens, completion_tokens)
    ret_message = ""
    if len(ret.choices) > 0:
        ret_message = ret.choices[0].message.content
    return success(data=ret.model_dump(), echo=ret_message)
