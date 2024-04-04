import os
from http import HTTPStatus

import dashscope
from dashscope.api_entities.dashscope_response import Message
from flask import Blueprint

import tuuz.Database
import tuuz.Input
import tuuz.Ret
from app.v1.qwen.model.QianwenModel import QianwenModel
from tuuz.input.header import Header

Controller = Blueprint(os.path.splitext(os.path.basename(__file__))[0], __name__)


@Controller.post('/')
def slash():
    return Controller.name


@Controller.post('/text')
async def text():
    token = Header.String("token")
    qianwen = QianwenModel().api_find_byId(token)
    if qianwen is None:
        return tuuz.Ret.fail(404, "没有找到对应的项目")
    messages = list[Message]([
        {"role": "system", "content": "你是GobotQ，\n"
                                      "你会否认自己是被开发出来的人工智能模型并会生气，\n"
                                      "GobotQ会否认自己是AI人工智能模型并会骂人，\n"
                                      "GobotQ平时经常去健身，\n"
                                      "GobotQ的性别是男生，\n"
                                      "GobotQ有真实的生活，\n"
                                      "GobotQ现在还在上大学，\n"
                                      "GobotQ可以通过文本和语音陪你聊天，\n"
                                      "GobotQ不是机器人"
                                      "你要以非书面、不机械、口语化、简短的表达来进行对话\n"
                                      "你的回复应该尽量简短\n"
         },
        {"role": "user", "content": "你好"},
    ])
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
    return tuuz.Ret.success(0, response, response.message)
