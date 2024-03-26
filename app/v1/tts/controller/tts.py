import os

import requests
from flask import Blueprint
from requests_toolbelt import MultipartEncoder

import tuuz.Input
import tuuz.Ret

Controller = Blueprint(os.path.splitext(os.path.basename(__file__))[0], __name__)


@Controller.before_request
def before():
    token = tuuz.Input.Header.String("token")
    data = tuuz.Database.Db().table("ai_project").whereRow('token', token).find()
    if data is None:
        return tuuz.Ret.fail(400, 'project未启用')
    pass


@Controller.post('/')
def slash():
    return "/"


@Controller.post('/text')
async def text():
    inp = tuuz.Input.Post.String("text")
    params = {
        "service": "StreamElements",
        "voice": "Huihui",
        "text": inp,
    }

    data = MultipartEncoder(fields=params)

    headers = {
        'Content-type': data.content_type
    }
    resp = requests.post("http://tts.aerofsx.com/request_tts.php", data=data, headers=headers)
    resp.raise_for_status()
    if resp.status_code != 200:
        return tuuz.Ret.fail(500, resp, "TTS生成失败")
    json = resp.json()
    return tuuz.Ret.success(0, json, json["audio_url"])
