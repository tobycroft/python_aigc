import os
from urllib.parse import urlparse

import ffmpeg
import pysilk
import requests
from flask import Blueprint
from urllib3.exceptions import InsecureRequestWarning

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
    response = requests.get(file, verify=False)
    response.raise_for_status()
    parsed_url = urlparse(file)
    filename = os.path.basename(parsed_url.path)
    dest_folder = "."
    file_path = os.path.join(dest_folder, filename)
    with open(file_path, "wb") as file:
        file.write(response.content)
    with open(file_path, "rb") as silk, open(filename + ".pcm", "wb") as pcm:
        pysilk.decode(silk, pcm, 44100)
    input_stream = ffmpeg.input(filename + ".pcm", format='s16le', ar=44100, ac=1)
    output_stream = ffmpeg.output(input_stream, filename + ".mp3")
    ffmpeg.run(output_stream)
    asr = BcutASR(filename + ".mp3")
    # asr = BcutASR('bb.wav')
    asr.upload()  # 上传文件
    asr.create_task()  # 创建任务
    os.remove(file_path)
    os.remove(file_path + ".pcm")
    os.remove(file_path + ".mp3")
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
        return tuuz.Ret.success(0, subtitle.to_srt(), subtitle.to_txt())
    return tuuz.Ret.fail(500, subtitle, '识别失败')


@Controller.post('/qq')
async def qq():
    file = tuuz.Input.Post.String("file")
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    response = requests.get(file, verify=False)
    response.raise_for_status()
    parsed_url = urlparse(file)
    filename = os.path.basename(parsed_url.path) + ".silk"
    dest_folder = "."
    file_path = os.path.join(dest_folder, filename)
    with open(file_path, "wb") as file:
        file.write(response.content)
    with open(file_path, "rb") as silk, open(filename + ".pcm", "wb") as pcm:
        pysilk.decode(silk, pcm, 44100)
    input_stream = ffmpeg.input(filename + ".pcm", format='s16le', ar=44100, ac=1)
    output_stream = ffmpeg.output(input_stream, filename + ".mp3")
    ffmpeg.run(output_stream)
    asr = BcutASR(filename + ".mp3")
    # asr = BcutASR('bb.wav')
    asr.upload()  # 上传文件
    asr.create_task()  # 创建任务
    os.remove(file_path)
    os.remove(file_path + ".pcm")
    os.remove(file_path + ".mp3")
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
        return tuuz.Ret.success(0, subtitle.to_srt(), subtitle.to_txt())
    return tuuz.Ret.fail(500, subtitle, '识别失败')
