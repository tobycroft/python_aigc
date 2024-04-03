from common.BaseModel import BaseModel
from tuuz import Database


class TokenModel(BaseModel):
    Table = 'token'

    def __init__(self, conn=None):
        super().__init__(conn)

    def Api_insert(self, uid, token, ip, type=None):
        if Database.Db(self.db).table(self.Table).insert({
            "uid": uid,
            'token': token,
            'ip': ip,
            'type': type
        }) is None:
            return False
        return True

    def Api_find_byToken(self, token):
        return Database.Db(self.db).table(self.Table).where('token', token).find()

    def Api_find_byUidAndToken(self, uid, token):
        return Database.Db(self.db).table(self.Table).where("uid", uid).where('token', token).find()
