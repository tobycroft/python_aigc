from flask import Blueprint

import tuuz.Input
import tuuz.Ret
import tuuz.database.database

Index = Blueprint('index', __name__)


@Index.route('/')
@Index.route('/index')
def index():
    print(tuuz.Input.Post.String("a"))
    data = tuuz.database.database.Db().table("coin").select()
    return tuuz.Ret.fail(400, data)
