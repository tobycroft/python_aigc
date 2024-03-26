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
        return flask.abort(204)

    if HEADER_AUTH_MODE:
        uid = Input.Header.String('uid')
        token = Input.Header.String('token')
        debug = Input.Header.String('debug')
    else:
        uid = Input.Post.String('uid')
        token = Input.Post.String('token')
        debug = Input.Post.String('debug')
    if TestMode:
        if debug == Debug:
            pass
    if TokenModel.Api_find_byUidAndToken(uid, token):
        pass
    else:
        return Ret.fail(-1, 'Auth_fail', '未登录')
