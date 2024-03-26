import os

from flask import Blueprint
from langchain_openai import OpenAI

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
    uid = Input.Header.Int('uid')
    llm = OpenAI(openai_api_key="YOUR_API_KEY", openai_organization="YOUR_ORGANIZATION_ID")
    Ret.success(0, 'success')
