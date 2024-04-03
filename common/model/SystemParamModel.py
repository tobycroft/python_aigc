from common.BaseModel import BaseModel
from tuuz import Database


class SystemParamModel(BaseModel):
    Table = 'system_param'

    def Api_find(self, key):
        return Database.Db(self.db).table(self.Table).where('key', key).find()

    def Api_find_value(self, key):
        return Database.Db(self.db).table(self.Table).where('key', key).value('value')
