from common.BaseModel import BaseModel
from tuuz import Database


class IflytekModel(BaseModel):
    Table = "ai_iflytek"

    def __init__(self, conn=None):
        super().__init__(conn)

    def api_find_byId(self, id):
        return Database.Db().table(self.Table).whereRow("id", id).find()
