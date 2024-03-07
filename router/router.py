from flask import Flask, Blueprint

import app.v1.index.route

v1 = Blueprint('v1', __name__)


@v1.route('/')
def version1():
    return 'v1'


def V1():
    v1.register_blueprint(app.v1.index.route.Route, url_prefix='/index')
    return v1


def MainRoute():
    global v1
    app = Flask(__name__)
    V1()
    app.register_blueprint(v1, url_prefix='/v1')
    return app
