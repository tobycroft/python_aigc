import os

import httpx
from flask import Blueprint
from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI

from app.v1.langchain.model import OpenAiModel
from common.controller.LoginController import LoginedController
from tuuz import Ret, Input

Controller = Blueprint(os.path.splitext(os.path.basename(__file__))[0], __name__)


@Controller.post('/')
def slash():
    return "/"


@Controller.before_request
def before_request():
    return LoginedController()


@Controller.post('text')
def text():
    uid = Input.Header.Int("uid")
    ai = OpenAiModel.Api_find(1)
    template = """Question: {question}

    Answer: Let's think step by step."""

    prompt = PromptTemplate.from_template(template)
    openai = OpenAI(openai_api_key=ai["key"], model_name="gpt-3.5-turbo-instruct", http_client=httpx.Client(proxies="https://fastgpt.ai.yaoyuankj.top"))
    # llm = OpenAI(openai_api_key=ai["key"])
    llm_chain = LLMChain(prompt=prompt, llm=openai)
    question = "What NFL team won the Super Bowl in the year Justin Beiber was born?"

    llm_chain.run(question)
    Ret.success(0, 'success')
