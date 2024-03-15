import os

from flask import Blueprint

import tuuz.Ret
from extend.bcut_asr import BcutASR, ResultStateEnum

Controller = Blueprint(os.path.splitext(os.path.basename(__file__))[0], __name__)


@Controller.post('/')
def slash():
    return "/"


@Controller.post('/audio')
async def audio():
    asr = BcutASR('http://image.tuuz.cc:81/gobotq/20240315/dd3d0790cf1ff7fc7e7adf878433c335.wav')
    # asr = BcutASR('bb.wav')
    asr.upload()  # 上传文件
    asr.create_task()  # 创建任务

    # 轮询检查结果
    while True:
        result = asr.result()
        # 判断识别成功
        if result.state == ResultStateEnum.COMPLETE:
            break

    # 解析字幕内容
    subtitle = result.parse()
    # 判断是否存在字幕
    if subtitle.has_data():
        # 输出srt格式
        print(subtitle.to_srt())
    return tuuz.Ret.success(0, subtitle.to_txt())
