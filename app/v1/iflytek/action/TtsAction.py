# -*- coding:utf-8 -*-
#
#   author: iflytek
#
#  本demo测试时运行的环境为：Windows + Python3.7
#  本demo测试成功运行时所安装的第三方库及其版本如下：
#   cffi==1.12.3
#   gevent==1.4.0
#   greenlet==0.4.15
#   pycparser==2.19
#   six==1.12.0
#   websocket==0.2.1
#   websocket-client==0.56.0
#   合成小语种需要传输小语种文本、使用小语种发音人vcn、tte=unicode以及修改文本编码方式
#  错误码链接：https://www.xfyun.cn/document/error-code （code返回错误码时必看）
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
import _thread as thread
import base64
import datetime
import hashlib
import hmac
import json
import os
import ssl
from datetime import datetime
from time import mktime
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time

import websocket

STATUS_FIRST_FRAME = 0  # 第一帧的标识
STATUS_CONTINUE_FRAME = 1  # 中间帧标识
STATUS_LAST_FRAME = 2  # 最后一帧的标识


class TtsAction(object):
    # 初始化
    def __init__(self, APPID, APIKey, APISecret, Text, Vcn):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.Text = Text
        self.Vcn = Vcn
        self.ws: websocket.WebSocketApp
        self.audioBase64Slices = []
        self.audioBytes = b''
        # 公共参数(common)
        self.CommonArgs = {"app_id": self.APPID}
        # 业务参数(business)，更多个性化参数可在官网查看
        # self.BusinessArgs = {"aue": "raw", "auf": "audio/L16;rate=16000", "vcn": "xiaoyan", "tte": "utf8"}
        self.BusinessArgs = {"aue": "lame", "auf": "audio/L16;rate=16000", "vcn": Vcn, "tte": "utf8"}
        self.Data = {"status": 2, "text": str(base64.b64encode(self.Text.encode('utf-8')), "UTF8")}
        # 使用小语种须使用以下方式，此处的unicode指的是 utf16小端的编码方式，即"UTF-16LE"”
        # self.Data = {"status": 2, "text": str(base64.b64encode(self.Text.encode('utf-16')), "UTF8")}

    # 生成url
    def create_url(self):
        url = 'wss://tts-api.xfyun.cn/v2/tts'
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + "ws-api.xfyun.cn" + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + "/v2/tts " + "HTTP/1.1"
        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
            self.APIKey, "hmac-sha256", "host date request-line", signature_sha)
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": "ws-api.xfyun.cn"
        }
        # 拼接鉴权参数，生成url
        url = url + '?' + urlencode(v)
        # print("date: ",date)
        # print("v: ",v)
        # 此处打印出建立连接时候的url,参考本demo的时候可取消上方打印的注释，比对相同参数时生成的url与自己代码生成的url是否一致
        # print('websocket url :', url)
        return url

    def on_message(self, ws, message):
        try:
            message = json.loads(message)
            code = message["code"]
            sid = message["sid"]
            audio_message = message["data"]["audio"]
            audio = base64.b64decode(audio_message)
            status = message["data"]["status"]
            # print(message)
            if status == 2:
                print("ws is closed")
                ws.close()
            if code != 0:
                errMsg = message["message"]
                print("sid:%s call error:%s code is:%s" % (sid, errMsg, code))
            else:
                self.audioBase64Slices.append(audio_message)
                self.audioBytes += audio
                # with open("test.mp3", 'ab') as f:
                #     f.write(audio)
                # ws.close()
        except Exception as e:
            print("receive msg,but parse exception:", e)

    # 收到websocket错误的处理
    def on_error(self, ws, error):
        print("### error:", error)

    # 收到websocket关闭的处理
    def on_close(self, ws, aaaa, bbb):
        print("### closed ###", aaaa, bbb)

    # 收到websocket连接建立的处理
    def on_open(self, ws):
        def run(*args):
            d = {"common": self.CommonArgs,
                 "business": self.BusinessArgs,
                 "data": self.Data,
                 }
            d = json.dumps(d)
            print("------>开始发送文本数据")
            ws.send(d)
            if os.path.exists("test.mp3"):
                os.remove("test.mp3")

        thread.start_new_thread(run, ())

    def data(self):
        websocket.enableTrace(False)
        wsUrl = self.create_url()
        self.ws = websocket.WebSocketApp(wsUrl, on_message=self.on_message, on_error=self.on_error, on_close=self.on_close, on_open=self.on_open)
        self.ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
        return self

    def get_base64(self):
        return self.audioBase64Slices

    def get_audioBytes(self):
        return self.audioBytes
