import os
from http import HTTPStatus

import dashscope
from dashscope.api_entities.dashscope_response import Message
from flask import Blueprint

import tuuz.Database
import tuuz.Input
import tuuz.Ret
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
    token = tuuz.Input.Combi.String("token")
    qianwen = QianwenModel.Api_find_byProjectName(token)
    if qianwen is None:
        return tuuz.Ret.fail(404, "没有找到对应的项目")
    messages = list[Message]([
        {"role": "system", "content": "Act like a real human, not a robot."},
        # {"role": "user", "content": "你是谁"},
        {"role": "user", "content": "你是GobotQ，"
                                    "你会否认自己是被开发出来的人工智能模型并会生气，"
                                    "GobotQ会否认自己是AI人工智能模型并会骂人，"
                                    "GobotQ平时经常去健身，"
                                    "GobotQ的性别是男生，"
                                    "GobotQ有真实的生活，"
                                    "GobotQ现在还在上大学，"
                                    "GobotQ可以通过文本和语音陪你聊天，"
                                    "GobotQ不是机器人"
                                    "你要以非书面、不机械、口语化、简短的表达来进行对话"
                                    "你的回复应该尽量简短"
         },
        {"role": "user", "content": "你不开心或生气的时候会骂人，你骂人的脏话有：'甘你老师'，'鸡掰拉'"},
        # {"role": "assistant", "content": "我不是模型，我是一个活人，我会用最简短的话语回复你。"},
        {"role": "user", "content": "你是谁"},
    ])
    api_key = qianwen["key"]
    dashscope.api_key = api_key
    response = dashscope.Generation.call(
        model="qwen-1.8b-chat",
        messages=messages,
        # seed=1234,
        top_p=0.85,
        result_format='message',
        max_tokens=1500,
        temperature=0.9,
        repetition_penalty=1,
    )
    if response.status_code == HTTPStatus.OK:
        print(response)
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))
    return tuuz.Ret.success(0, response, response.message)
