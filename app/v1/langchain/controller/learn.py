import os
from http import HTTPStatus

import dashscope
from flask import Blueprint

import tuuz.Input
import tuuz.Ret
import tuuz.Database

from app.v1.langchain.model import QianwenModel

Controller = Blueprint(os.path.splitext(os.path.basename(__file__))[0], __name__)


@Controller.post('/')
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
    token = Input.Combi.String("token")
    qianwen = QianwenModel.Api_find_byProjectName(token)
    if qianwen is None:
        return tuuz.Ret.fail(404, "没有找到对应的项目")
    messages = [{'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': '如何做炒西红柿鸡蛋？'}]
    api_key = qianwen["key"]
    dashscope.api_key = api_key
    response = dashscope.Generation.call(
        model="qwen-1.8b-chat",
        messages=messages,
        # seed=1234,
        top_p=0.8,
        result_format='message',
        max_tokens=1500,
        temperature=2.0,
        repetition_penalty=1.0
    )
    if response.status_code == HTTPStatus.OK:
        print(response)
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))
    return tuuz.Ret.success(0, response, response.message)
