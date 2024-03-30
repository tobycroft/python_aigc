import bleach
from flask import request, abort, make_response

from tuuz.Ret import fail


class Header:

    @staticmethod
    def Str(key: str, need_xss=False):
        return Header.String(key, need_xss)

    @staticmethod
    def String(key: str, need_xss=False):
        in_data = request.headers.get(key)
        if in_data is None:
            abort(make_response(fail(400, echo="Header-[" + key + "]")))
        else:
            if need_xss:
                out = bleach.clean(in_data, tags=[], attributes={}, strip=False, strip_comments=True)
                return out
            else:
                return in_data

    @staticmethod
    def Int(key: str) -> object:
        in_data = request.headers.get(key)
        if not in_data:
            abort(make_response(fail(400, echo=f"Header-[{key}] not found")))
        try:
            return int(in_data)
        except ValueError:
            abort(make_response(fail(400, echo=f"Header-[{key}] is not " + __name__)))

    @staticmethod
    def Float(key: str):
        in_data = request.headers.get(key)
        if not in_data:
            abort(make_response(fail(400, echo=f"Header-[{key}] not found")))
        try:
            return float(in_data)
        except ValueError:
            abort(make_response(fail(400, echo=f"Header-[{key}] is not " + __name__)))

    @staticmethod
    def Bool(key: str) -> bool:
        in_data = request.headers.get(key)
        if not in_data:
            abort(make_response(fail(400, echo=f"Header-[{key}] not found")))
        try:
            return bool(int(in_data))
        except ValueError:
            abort(make_response(fail(400, echo=f"Header-[{key}] is not " + __name__)))
