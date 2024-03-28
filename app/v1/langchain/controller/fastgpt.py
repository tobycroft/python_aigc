import os

import langchain_openai
from flask import Blueprint

from common.controller.LoginController import LoginedController
from tuuz import Ret, Input

Controller = Blueprint(os.path.splitext(os.path.basename(__file__))[0], __name__)


@Controller.post('/')
def slash():
    return Controller.name


@Controller.before_request
def before_request():
    return LoginedController()


@Controller.post('text')
def text():
    uid = Input.Header.Int("uid")
    # ai = OpenAiModel.Api_find(1)
    # template = """Question: {question}
    #
    # Answer: Let's think step by step."""

    # prompt = PromptTemplate.from_template(template)
    # print(ai["key"])
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
