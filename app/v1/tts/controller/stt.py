import base64
import hashlib
import os
from urllib.parse import urlparse

import ffmpeg
import pysilk
import requests
from flask import Blueprint
from urllib3.exceptions import InsecureRequestWarning

from tuuz import Ret, Input, Database
from extend.bcut_asr import BcutASR, ResultStateEnum

Controller = Blueprint(os.path.splitext(os.path.basename(__file__))[0], __name__)


@Controller.before_request
def before():
    token = Input.Header.String("token")
    data = Database.Db().table("ai_project").where('token', token).find()
    if data is None:
        return Ret.fail(400, 'project未启用')
    pass


@Controller.post('/')
def slash():
    return Controller.name


@Controller.post('/audio')
async def audio():
    file = Input.Post.String("file")
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
        return Ret.success(0, subtitle.to_srt(), subtitle.to_txt())
    return Ret.fail(500, subtitle, '识别失败')


@Controller.post('/qq')
async def qq():
    url = Input.Post.String("url")
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    response = requests.get(url, verify=False)
    response.raise_for_status()
    print(response.content)
    file_md5 = hashlib.md5()
    file_md5.update(url.encode('utf-8'))
    filename = file_md5.hexdigest() + ".silk"
    dest_folder = "."
    file_path = os.path.join(dest_folder, filename)
    with open(file_path, "wb") as url:
        url.write(response.content)
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
        return Ret.success(0, subtitle.to_srt(), subtitle.to_txt())
    return Ret.fail(500, None, '识别失败')


@Controller.post('/b64')
async def b64():
    b64 = Input.Post.String("base64")
    base64_decode = base64.b64decode(b64)
    dest_folder = "."
    hashlib.md5()
    file_md5 = hashlib.md5()
    file_md5.update(b64.encode('utf-8'))
    filename = file_md5.hexdigest() + ".mp3"
    file_path = os.path.join(dest_folder, filename)
    with open(file_path, "wb") as fb:
        fb.write(base64_decode)
    asr = BcutASR(filename)
    # asr = BcutASR('bb.wav')
    asr.upload()  # 上传文件
    asr.create_task()  # 创建任务
    os.remove(file_path)
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
        return Ret.success(0, subtitle.to_srt(), subtitle.to_txt())
    return Ret.fail(500, None, '识别失败')
