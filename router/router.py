import flask
from flask import Flask
from flask_cors import CORS

import app.v1.route


def MainRoute():
    fk = Flask(__name__)
    print("flask_version:", flask.__version__)
    CORS(fk, max_age=3600, supports_credentials=True)
    fk.register_blueprint(app.v1.route.Route, url_prefix="/v1")
    return fk
