import os

from flask import Blueprint
from transformers import BertTokenizer, BertForMaskedLM, BertConfig

import tuuz.Ret

Controller = Blueprint(os.path.splitext(os.path.basename(__file__))[0], __name__)


@Controller.before_request
def before():
    token = tuuz.Input.Combi.String("token")
    data = tuuz.Database.Db().table("ai_project").whereRow('token', token).find()
    if data is None:
        return tuuz.Ret.fail(400, 'project未启用')
    pass
@Controller.post('/')
def slash():
    return "/"



@Controller.post('/text')
async def text():
    # 加载tokenizer

    return tuuz.Ret.success(0, )
