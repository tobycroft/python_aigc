#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author : iflytek

import base64
import hashlib
import hmac
import json
import logging
import time
from datetime import datetime
from time import mktime
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time

import requests
from ws4py.client.threadedclient import WebSocketClient

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

################init 参数######################
# 音频驱动参数
STATUS_FIRST_FRAME = 0  # 第一帧的标识
STATUS_CONTINUE_FRAME = 1  # 中间帧标识
STATUS_LAST_FRAME = 2  # 最后一帧的标识


# 用户参数，相关参数注意修改

###############################################


class RequestParam(object):

    def __init__(self, HOST, APP_ID, API_KEY, API_SECRET):
        self.host = HOST
        self.app_id = APP_ID
        self.api_key = API_KEY
        self.api_secret = API_SECRET

    # 生成鉴权的url
    def assemble_auth_url(self, path, method='POST', schema='http'):
        params = self.assemble_auth_params(path, method)
        # 请求地址
        request_url = "%s://" % schema + self.host + path
        # 拼接请求地址和鉴权参数，生成带鉴权参数的url
        auth_url = request_url + "?" + urlencode(params)
        return auth_url

    # 生成鉴权的参数
    def assemble_auth_params(self, path, method):
        # 生成RFC1123格式的时间戳
        format_date = format_date_time(mktime(datetime.now().timetuple()))
        # 拼接字符串
        signature_origin = "host: " + self.host + "\n"
        signature_origin += "date: " + format_date + "\n"
        signature_origin += method + " " + path + " HTTP/1.1"
        # 进行hmac-sha256加密
        signature_sha = hmac.new(self.api_secret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')
        # 构建请求参数
        authorization_origin = 'api_key="%s", algorithm="%s", headers="%s", signature="%s"' % (
            self.api_key, "hmac-sha256", "host date request-line", signature_sha)
        # 将请求参数使用base64编码
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        # 将请求的鉴权参数组合为字典
        params = {
            "host": self.host,
            "date": format_date,
            "authorization": authorization
        }
        return params


class VmsApi(RequestParam):
    # 接口data请求参数，字段具体含义见官网文档
    # 启动
    def start(self, start_url):
        data = {
            "header": {
                "app_id": self.app_id,
                "uid": ""
            },
            "parameter": {
                "vmr": {
                    "stream": {
                        "protocol": "rtmp"
                    },
                    "avatar_id": "110029003",  # 110029002
                    "width": 1280,
                    "height": 720
                }
            }
        }
        url_data = self.get_url_data(start_url, data)
        session = ''
        if url_data:
            session = url_data.get('header', {}).get('session', '')
            stream_url = url_data.get('header', {}).get('stream_url', '拉流地址获取失败')
            print("拉流地址：%s" % stream_url)
            return session

    # 心跳
    def ping(self, ping_url, session):
        data = {
            "header": {
                "app_id": self.app_id,
                "uid": "",
                "session": session
            }
        }
        self.get_url_data(ping_url, data)

    # 停止
    def stop(self, stop_url, session):
        data = {
            "header": {
                "app_id": self.app_id,
                "session": session,
                "uid": ""
            }
        }
        self.get_url_data(stop_url, data)

    # 文本驱动
    def text_ctrl(self, text_url, session, text):
        # 合成文本
        encode_str = base64.encodebytes(text.encode("UTF8"))
        txt = encode_str.decode()
        data = {
            "header": {
                "app_id": self.app_id,
                "session": session,
                "uid": ""
            },
            "parameter": {
                "tts": {
                    "vcn": "x3_yezi",  # x3_qianxue
                    "speed": 40,
                    "pitch": 50,
                    "volume": 50
                }
            },
            "payload": {
                "text": {
                    "encoding": "utf8",
                    "status": 3,
                    "text": txt
                },
                "ctrl_w": {
                    "encoding": "utf8",
                    "format": "json",
                    "status": 3,
                    # "text": ""
                }
            }
        }
        self.get_url_data(text_url, data)
        print("请求参数：", json.dumps(data))

    # 音频驱动
    def audio_ctrl(self, audio_url, session, audio_file):
        auth_audio_url = self.assemble_auth_url(audio_url, 'GET', 'ws')
        ws = AudioCtrl(auth_audio_url, session, audio_file)
        ws.connect()
        ws.run_forever()

    def get_url_data(self, url, data):
        auth_url = self.assemble_auth_url(url)
        print("示例url:", auth_url)
        headers = {'Content-Type': 'application/json'}
        try:
            result = requests.post(url=auth_url, headers=headers, data=json.dumps(data))
            result = json.loads(result.text)
            print("response:", json.dumps(result))
            code = result.get('header', {}).get('code')
            if code == 0:
                logging.info("%s 接口调用成功" % url)
                return result
            else:
                logging.error("%s 接口调用失败，错误码:%s" % (url, code))
                return {}
        except Exception as e:
            logging.error("%s 接口调用异常，错误详情:%s" % (url, e))
            return {}


# websocket 音频驱动
class AudioCtrl(WebSocketClient):

    def __init__(self, url, session, file_path):
        super().__init__(url)
        self.file_path = file_path
        self.session = session
        self.app_id = APP_ID

    # 收到websocket消息的处理
    def received_message(self, message):
        message = message.__str__()
        try:
            res = json.loads(message)
            print("response:", json.dumps(res))
            # 音频驱动接口返回状态码
            code = res.get('header', {}).get('code')
            # 状态码为0，音频驱动接口调用成功
            if code == 0:
                logging.info("音频驱动接口调用成功")
            # 状态码非0，音频驱动接口调用失败, 相关错误码参考官网文档
            else:
                logging.info("音频驱动接口调用失败，返回状态码: %s" % code)
        except Exception as e:
            logging.info("音频驱动接口调用失败，错误详情:%s" % e)

    # 收到websocket错误的处理
    def on_error(self, error):
        logging.error(error)

    # 收到websocket关闭的处理
    def closed(self, code, reason=None):
        logging.info('音频驱动：websocket关闭')

    # 收到websocket连接建立的处理
    def opened(self):
        logging.info('音频驱动：websocket连接建立')
        frame_size = 1280  # 每一帧音频大小
        interval = 0.04  # 发送音频间隔(单位:s)
        status = STATUS_FIRST_FRAME  # 音频的状态信息，标识音频是第一帧，还是中间帧、最后一帧
        count = 1
        with open(self.file_path, 'rb') as file:
            while True:
                buffer = file.read(frame_size)
                if len(buffer) < frame_size:
                    status = STATUS_LAST_FRAME
                # 第一帧处理
                if status == STATUS_FIRST_FRAME:
                    self.send_frame(status, buffer, count)
                    status = STATUS_CONTINUE_FRAME
                # 中间帧处理
                elif status == STATUS_CONTINUE_FRAME:
                    self.send_frame(status, buffer, count)

                # 最后一帧处理
                elif status == STATUS_LAST_FRAME:
                    self.send_frame(status, buffer, count)
                    break
                count += 1
                # 音频采样间隔
                time.sleep(interval)

    # 发送音频
    def send_frame(self, status, audio_buffer, seq):
        data = {
            "header": {
                "app_id": self.app_id,
                "session": self.session,
                "status": status,
                "uid": ""
            },
            "payload": {
                "audio": {
                    "encoding": "raw",
                    "sample_rate": 16000,
                    "status": status,
                    "seq": seq,
                    "audio": base64.encodebytes(audio_buffer).decode("utf-8")
                }
            }
        }
        json_data = json.dumps(data)
        print("请求参数：", json_data)
        self.send(json_data)


if __name__ == "__main__":
    vms = VmsApi()
    start_url = "/v1/private/vms2d_start"
    print("启动")
    session = vms.start(start_url)

    if session:
        # 文本驱动，自定义文本内容
        time.sleep(10)
        print("\n文本驱动")
        text = "你好，有什么可以帮助你的？"
        text_url = "/v1/private/vms2d_ctrl"
        vms.text_ctrl(text_url, session, text)

        # 音频驱动
        # time.sleep(10)
        # print("\n音频驱动")
        audio_url = "/v1/private/vms2d_audio_ctrl"
        audio_file = "tts.mp3"
        # vms.audio_ctrl(audio_url, session, audio_file)

        # 心跳
        # time.sleep(10)
        # print("\n心跳")
        ping_url = "/v1/private/vms2d_ping"
        # vms.ping(ping_url, session)

        # 文本驱动

        while text != "再见":
            text = input("请输入文本：")
            test = text.encode("utf-8").decode("latin1")

            # conn = http.client.HTTPSConnection("api.link-ai.chat")
            # payload = "{\n  \"app_code\": \"default\",\n  \"messages\": [\n    {\n      \"role\": \"user\",\n      \"content\": "+ text +"\n    }\n  ]\n}"
            # headers = {
            #    'Content-Type': "application/json",
            #     'Authorization': "Bearer Link_7Vv9LnL0cBkPyhJLedj7XmhwTHJ3aFbwIpdP47G7fR"
            #    }
            # conn.request("POST", "/v1/chat/completions", payload, headers)
            # res = conn.getresponse()
            # data = res.read()

            # res_content=data['choices']['message']['content']
            # text=res_content.decode("utf-8")
            # print(text)

            vms.ping(ping_url, session)
            vms.text_ctrl(text_url, session, text)

        # 停止
        # time.sleep(10)
        # print("\n停止")
        # stop_url = "/v1/private/vms2d_stop"
        # vms.stop(stop_url, session)
