from flask import Blueprint
from transformers import DistilBertTokenizer, DistilBertForMaskedLM

StudyController = Blueprint("gemini", __name__)


@StudyController.route('/')
def slash():
    return "/"


@StudyController.post('/text')
async def text():
    # 加载DistilBERT模型和tokenizer
    model_name = "distilbert-base-uncased"
    tokenizer = DistilBertTokenizer.from_pretrained(model_name)
    model = DistilBertForMaskedLM.from_pretrained(model_name)

    # 定义一个填空句子
    text = "I like to eat [MASK]."

    # 使用tokenizer对文本进行编码
    inputs = tokenizer(text, return_tensors="pt")

    # 预测缺失的词语
    outputs = model(**inputs)
    predictions = outputs.logits.argmax(dim=-1)

    # 将预测的词语解码成文本
    predicted_token = tokenizer.decode(predictions[0][3].item())

    print("原句子:", text)
    print("填空后的句子:", text.replace("[MASK]", predicted_token))
