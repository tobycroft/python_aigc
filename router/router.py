from flask import Flask

import app.v1.route


def MainRoute():
    fk = Flask(__name__)
    fk.register_blueprint(app.v1.route.Route, url_prefix="/v1")
    return fk
