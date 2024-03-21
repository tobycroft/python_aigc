import os
from http import HTTPStatus

import dashscope
from flask import Blueprint

import Input
import tuuz.Ret
from app.v1.langchain.model import QianwenModel

Controller = Blueprint(os.path.splitext(os.path.basename(__file__))[0], __name__)


@Controller.post('/')
def slash():
    return "/"


@Controller.post('/text')
async def text():
    token = Input.Combi.String("token")
    if QianwenModel.Api_find_byProjectName(token) is None:
        return tuuz.Ret.fail(404, "没有找到对应的项目")
    messages = [{'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': '如何做炒西红柿鸡蛋？'}]

    response = dashscope.Generation.call(
        dashscope.Generation.Models.qwen_turbo,
        messages=messages,
        result_format='message',  # set the result to be "message" format.
    )
    if response.status_code == HTTPStatus.OK:
        print(response)
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))
    return tuuz.Ret.success(0, )
