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
    tokenizer = BertTokenizer.from_pretrained("I:/llama2/")

    # 加载配置文件
    config = BertConfig.from_pretrained("I:/llama2/config.json")

    # 加载模型
    model = BertForMaskedLM.from_pretrained("I:/llama2/pytorch_model.bin", config=config)


    # 初始化对话处理器和生成器
    processor = ConversationProcessor(tokenizer=tokenizer)
    generator = ConversationGenerator(model=model, processor=processor)
    return tuuz.Ret.success(0, text)
