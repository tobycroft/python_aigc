import os

from flask import Blueprint

import tuuz.Input
import tuuz.Ret
from extend.bcut_asr import BcutASR, ResultStateEnum

Controller = Blueprint(os.path.splitext(os.path.basename(__file__))[0], __name__)


@Controller.post('/')
def slash():
    return "/"


@Controller.post('/audio')
async def audio():
    file = tuuz.Input.Post.String("file")
    asr = BcutASR(file)
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
