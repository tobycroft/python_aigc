import os

from flask import Blueprint

from app.v1.live2d.model.Live2dTipsModel import Live2dTipsModel
from tuuz import Ret
from tuuz.Ret import success

Controller = Blueprint(os.path.splitext(os.path.basename(__file__))[0], __name__)


@Controller.post('/')
def slash():
    return Controller.name


@Controller.post('index')
async def index():
    return Ret.success(0)


# list

@Controller.post('list')
async def list_tips():
    tips_data = Live2dTipsModel().api_select()
    tips_dict = {}
    for tip in tips_data:
        tip_type = tip['type']
        if tip_type not in tips_dict:
            tips_dict[tip_type] = []
        tip_entry = {
            'selector': tip['selector'],
            'texts': eval(tip['texts'])  # Assuming texts are stored as JSON strings in the database
        }
        tips_dict[tip_type].append(tip_entry)
    return success(data=tips_dict)
