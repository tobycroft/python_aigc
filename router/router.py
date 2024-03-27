from sanic import Sanic
from sanic_cors import CORS

import config.app
from app.v1.route import v1


def main_route() -> Sanic:
    sk = Sanic(name=config.app.Project)
    CORS(sk)
    # print("flask_version:", Sanic.__version__)
    # sk.register_middleware(add_cors_headers, "response")
    sk.blueprint(v1)
    return sk
