import bleach
from flask import request, abort, make_response

from tuuz.Ret import fail


class Get:

    @staticmethod
    def Str(key: str, need_xss=False):
        return Get.String(key, need_xss)

    @staticmethod
    def String(key: str, need_xss=False):
        in_data = request.args.get(key)
        if not in_data:
            abort(make_response(fail(400, echo=f"GET-[{key}] not found")))
        else:
            if need_xss:
                out = bleach.clean(in_data, tags=[], attributes={}, strip=False, strip_comments=True)
                return out
            else:
                return in_data

    @staticmethod
    def Int(key: str):
        in_data = request.args.get(key)
        if not in_data:
            abort(make_response(fail(400, echo=f"GET-[{key}] not found")))
        try:
            return int(in_data)
        except ValueError:
            abort(make_response(fail(400, echo=f"GET-[{key}] is not an integer")))

    @staticmethod
    def Float(key: str):
        in_data = request.args.get(key)
        if not in_data:
            abort(make_response(fail(400, echo=f"GET-[{key}] not found")))
        try:
            return float(in_data)
        except ValueError:
            abort(make_response(fail(400, echo=f"GET-[{key}] is not a float")))

    @staticmethod
    def Bool(key: str) -> bool:
        in_data = request.args.get(key)
        if not in_data:
            abort(make_response(fail(400, echo=f"GET-[{key}] not found")))
        try:
            return bool(int(in_data))
        except ValueError:
            abort(make_response(fail(400, echo=f"GET-[{key}] is not a boolean")))
