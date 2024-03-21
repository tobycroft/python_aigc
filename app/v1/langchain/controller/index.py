import os

from flask import Blueprint
from transformers import BertTokenizer, BertForMaskedLM, BertConfig

import tuuz.Ret

Controller = Blueprint(os.path.splitext(os.path.basename(__file__))[0], __name__)


@Controller.post('/')
def slash():
    return "/"


@Controller.post('/text')
async def text():
    # 加载tokenizer

    return tuuz.Ret.success(0, )
