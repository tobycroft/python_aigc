import bleach
from flask import request, make_response, abort

import tuuz.Ret


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
            abort(make_response(tuuz.Ret.fail(400, echo="Unsupported request method")))

        if not in_data:
            abort(make_response(tuuz.Ret.fail(400, echo="POST-[" + key + "]")))
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
            abort(make_response(tuuz.Ret.fail(400, echo="Unsupported request method")))

        if not in_data:
            abort(make_response(tuuz.Ret.fail(400, echo=f"POST-[{key}] not found")))
        try:
            return int(in_data)
        except ValueError:
            abort(make_response(tuuz.Ret.fail(400, echo=f"POST-[{key}] is not " + __name__)))

    @staticmethod
    def Float(key: str):
        if request.method == 'GET':
            in_data = request.args.get(key)
        elif request.method == 'POST':
            in_data = request.form.get(key)
        else:
            abort(make_response(tuuz.Ret.fail(400, echo="Unsupported request method")))

        if not in_data:
            abort(make_response(tuuz.Ret.fail(400, echo=f"POST-[{key}] not found")))
        try:
            return float(in_data)
        except ValueError:
            abort(make_response(tuuz.Ret.fail(400, echo=f"POST-[{key}] is not " + __name__)))

    @staticmethod
    def Bool(key: str) -> bool:
        if request.method == 'GET':
            in_data = request.args.get(key)
        elif request.method == 'POST':
            in_data = request.form.get(key)
        else:
            abort(make_response(tuuz.Ret.fail(400, echo="Unsupported request method")))

        if not in_data:
            abort(make_response(tuuz.Ret.fail(400, echo=f"POST-[{key}] not found")))
        try:
            return bool(int(in_data))
        except ValueError:
            abort(make_response(tuuz.Ret.fail(400, echo=f"POST-[{key}] is not " + __name__)))


class Post(Combi):
    pass


class Get(Combi):
    pass


class Header:

    @staticmethod
    def Str(key: str, need_xss=False):
        return Header.String(key, need_xss)

    @staticmethod
    def String(key: str, need_xss=False):
        in_data = request.headers.get(key)
        if not in_data:
            abort(make_response(tuuz.Ret.fail(400, echo="Header-[" + key + "]")))
        else:
            if need_xss:
                out = bleach.clean(in_data, tags=[], attributes={}, strip=False, strip_comments=True)
                return out
            else:
                return in_data

    @staticmethod
    def Int(key: str):
        in_data = request.headers.get(key)
        if not in_data:
            abort(make_response(tuuz.Ret.fail(400, echo=f"Header-[{key}] not found")))
        try:
            return int(in_data)
        except ValueError:
            abort(make_response(tuuz.Ret.fail(400, echo=f"Header-[{key}] is not " + __name__)))

    @staticmethod
    def Float(key: str):
        in_data = request.headers.get(key)
        if not in_data:
            abort(make_response(tuuz.Ret.fail(400, echo=f"Header-[{key}] not found")))
        try:
            return float(in_data)
        except ValueError:
            abort(make_response(tuuz.Ret.fail(400, echo=f"Header-[{key}] is not " + __name__)))

    @staticmethod
    def Bool(key: str) -> bool:
        in_data = request.headers.get(key)
        if not in_data:
            abort(make_response(tuuz.Ret.fail(400, echo=f"Header-[{key}] not found")))
        try:
            return bool(int(in_data))
        except ValueError:
            abort(make_response(tuuz.Ret.fail(400, echo=f"Header-[{key}] is not " + __name__)))
