import flask
from flask import request

from common.model import TokenModel
from config.app import TestMode, Debug
from config.secure import HEADER_AUTH_MODE
from tuuz import Input, Ret


def LoginedController():
    global uid, token, debug
    uid = ""
    token = ""
    debug = ""
    if request.method == 'OPTIONS':
        return flask.abort(200)

    if HEADER_AUTH_MODE:
        uid = Input.Header.Int("uid")
        token = Input.Header.String('token')
        debug = request.headers.get("debug")
    else:
        uid = Input.Post.Int("uid")
        token = Input.Post.String('token')
        debug = request.form.get("debug")

    if TestMode:
        if debug == Debug:
            return
    if TokenModel.Api_find_byUidAndToken(uid, token):
        return
    else:
        return Ret.fail(-1, 'Auth_fail', '未登录')
