import bleach
from flask import request, abort, make_response

from tuuz.Ret import fail


class Combi:

    @staticmethod
    def Str(key: str, need_xss=False):
        return Combi.String(key, need_xss)

    @staticmethod
    def String(key: str, need_xss=False):
        if request.method == 'GET':
            in_data = request.args.get(key)
        elif request.method == 'POST':
            in_data = request.form.get(key)
        else:
            abort(make_response(fail(400, echo="Unsupported request method")))

        if in_data is None:
            abort(make_response(fail(400, echo="GET/POST-[" + key + "]")))
        else:
            if need_xss:
                out = bleach.clean(in_data, tags=[], attributes={}, strip=False, strip_comments=True)
                return out
            else:
                return in_data

    @staticmethod
    def Int(key: str):
        if request.method == 'GET':
            in_data = request.args.get(key)
        elif request.method == 'POST':
            in_data = request.form.get(key)
        else:
            abort(make_response(fail(400, echo="Unsupported request method")))

        if not in_data:
            abort(make_response(fail(400, echo=f"GET/POST-[{key}] not found")))
        try:
            return int(in_data)
        except ValueError:
            abort(make_response(fail(400, echo=f"GET/POST-[{key}] is not " + __name__)))

    @staticmethod
    def Float(key: str):
        if request.method == 'GET':
            in_data = request.args.get(key)
        elif request.method == 'POST':
            in_data = request.form.get(key)
        else:
            abort(make_response(fail(400, echo="Unsupported request method")))

        if not in_data:
            abort(make_response(fail(400, echo=f"GET/POST-[{key}] not found")))
        try:
            return float(in_data)
        except ValueError:
            abort(make_response(fail(400, echo=f"GET/POST-[{key}] is not " + __name__)))

    @staticmethod
    def Bool(key: str) -> bool:
        if request.method == 'GET':
            in_data = request.args.get(key)
        elif request.method == 'POST':
            in_data = request.form.get(key)
        else:
            abort(make_response(fail(400, echo="Unsupported request method")))

        if not in_data:
            abort(make_response(fail(400, echo=f"GET/POST-[{key}] not found")))
        try:
            return bool(int(in_data))
        except ValueError:
            abort(make_response(fail(400, echo=f"GET/POST-[{key}] is not " + __name__)))
