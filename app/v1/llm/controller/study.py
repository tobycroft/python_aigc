from flask import Blueprint
from transformers import BertTokenizer, BertForMaskedLM, BertConfig

import tuuz.Ret

StudyController = Blueprint(__file__, __name__)


@StudyController.post('/')
def slash():
    return "/"


@StudyController.post('/text')
async def text():
    # 加载tokenizer

    return tuuz.Ret.success(0, )
