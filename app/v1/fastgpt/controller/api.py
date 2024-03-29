import os

import flask
from flask import Blueprint
from openai import OpenAI

from app.v1.coin.action.CoinCalcAction import CoinCalcAction
from app.v1.coin.model.CoinModel import CoinModel
from app.v1.fastgpt.model.FastgptModel import FastgptModel
from app.v1.team.model.TeamSubtokenModel import TeamSubtokenModel
from common.controller.LoginController import LoginedController
from tuuz import Ret
from tuuz.Input import Header, Post
from tuuz.Ret import json_response

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
    id = Post.Int("id")
    subtoken = TeamSubtokenModel().api_find_byUidAndId(uid, id)
    if not subtoken:
        return Ret.fail(404, echo="没有找到对应的key")
    if int(subtoken["is_limit"]) == 1 and float(subtoken["amount"]) <= 0:
        return Ret.fail(403, echo="你的key已经没有余量了，请在控制台增加余量或将key设定为无限量模式")
    if subtoken["coin_id"] != 5:
        coin_name = ""
        coin = CoinModel().api_find(subtoken["coin_id"])
        if coin:
            coin_name = coin["name"]
        return Ret.fail(404, echo="key只能使用于" + coin_name)
    fastgpt = FastgptModel().api_find_byId(subtoken["from_id"])
    if not fastgpt:
        return Ret.fail(404, echo="FastGPT中的上级Key被删除")
    client = OpenAI(api_key=fastgpt["key"], base_url=fastgpt["base_url"])
    ret = client.chat.completions.create(
        model=fastgpt["model"],
        messages=flask.request.json.get("messages"),
        response_format={"type": "json_object"},
        extra_body={
            "chatId": flask.request.json.get("chatId"),
            "detail": fastgpt["detail"],
        }
        # temperature=0,
    )
    total_tokens = ret.usage.total_tokens
    prompt_tokens = ret.usage.prompt_tokens
    completion_tokens = ret.usage.completion_tokens

    used_price = CoinCalcAction(subtoken["coin_id"]).Calc(total_tokens)
    TeamSubtokenModel().api_inc_amount_byKey(subtoken["key"], -abs(used_price))

    # print(ret.model_dump(), total_tokens, prompt_tokens, completion_tokens)
    return json_response(ret.model_dump())
