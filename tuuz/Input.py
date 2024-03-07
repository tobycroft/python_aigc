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
                return out, True
            else:
                return in_data, True
