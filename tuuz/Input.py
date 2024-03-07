import flask
from flask import request, make_response

import tuuz.Ret


class Post:
    @staticmethod
    def String(key, need_xss=False):
        in_data = request.form.get(key)
        if not in_data:
            flask.abort(make_response(tuuz.Ret.fail(400, echo="POST-[" + key + "]")))
        else:
            if need_xss:
                # TODO: 需要完成xss过滤这里
                out = (in_data)
                return out
            else:
                return in_data


class Get:
    @staticmethod
    def String(key, need_xss=False):
        in_data = request.args.get(key)
        if not in_data:
            flask.abort(make_response(tuuz.Ret.fail(400, echo="GET-[" + key + "]")))
        else:
            if need_xss:
                # TODO: 需要完成xss过滤这里
                out = (in_data)
                return out
            else:
                return in_data


class Combi:
    @staticmethod
    def String(key, need_xss=False):
        in_data = request.form.get(key)
        if not in_data:
            in_data = request.args.get(key)
        if not in_data:
            flask.abort(make_response(tuuz.Ret.fail(400, echo="COMBI-[" + key + "]")))
        else:
            if need_xss:
                # TODO: 需要完成xss过滤这里
                out = (in_data)
                return out
            else:
                return in_data
