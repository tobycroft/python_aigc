import os

from flask import Blueprint
from paddlespeech.cli.tts.infer import TTSExecutor

import tuuz.Ret

Controller = Blueprint(os.path.splitext(os.path.basename(__file__))[0], __name__)


@Controller.post('/')
def slash():
    return "/"


@Controller.post('/text')
async def text():
    # 加载tokenizer
    tts = TTSExecutor()
    tts(text="今天天气十分不错。", output="output.wav")
    return tuuz.Ret.success(0, )
