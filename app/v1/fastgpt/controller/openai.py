import os

from flask import Blueprint

from app.v1.team.model.TeamSubtokenModel import TeamSubtokenModel
from tuuz import Ret
from tuuz.Input import Header

Controller = Blueprint(os.path.splitext(os.path.basename(__file__))[0], __name__)


@Controller.post('/')
def slash():
    return "/"


@Controller.before_request
def before_request():
    Authorization = Header.Str("Authorization")
    try:
        auth = Authorization.replace("Bearer ", "").split('-')
        prefix = auth[0]
        key = auth[1]
    except Exception as e:
        return Ret.fail(401, e, echo="Authorization头不正确")
    ts = TeamSubtokenModel().api_find_byKey(key)
    if not ts:
        return Ret.fail(404, echo="没有找到对应的key")


@Controller.post('text')
def text():
    # uid = Header.Int("uid")
    # a = langchain_openai.ChatOpenAI(api_key=ai["key"], base_url="https://fastgpt.ai.yaoyuankj.top/api/v1")
    # ret = a.invoke("What NFL team won the Super Bowl in the year Justin Beiber was born?")
    # print(ret)
    # openai = OpenAIChat(api_key=ai["key"], base_url="https://fastgpt.ai.yaoyuankj.top/api/v1")
    # openai.invoke("What NFL team won the Super Bowl in the year Justin Beiber was born?")
    # openai = OpenAI(openai_api_key=ai["key"])
    # llm_chain = LLMChain(prompt=prompt, llm=openai)
    # question = "What NFL team won the Super Bowl in the year Justin Beiber was born?"
    #
    # llm_chain.invoke({"question": question})
    # embeddings = OpenAIEmbeddings(model="text-embedding-3-large", openai_api_key=ai["key"], openai_api_base="https://fastgpt.ai.yaoyuankj.top/api/v1")
    #
    # text = "This is a test document."
    # query_result = embeddings.embed_query(text)
    # print(query_result)
    Ret.success(0, 'success')
