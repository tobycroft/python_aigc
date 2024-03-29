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
        return flask.make_response('', 204)

    if HEADER_AUTH_MODE:
        uid = request.headers.get("uid")
        token = request.headers.get('token')
        debug = request.headers.get("debug")
    else:
        uid = request.form.get("uid")
        token = request.form.get('token')
        debug = request.form.get("debug")

    if TestMode:
        if debug == Debug:
            return
    if TokenModel.Api_find_byUidAndToken(uid, token):
        return
    else:
        return Ret.fail(-1, 'Auth_fail', '未登录')
