from common.BaseModel import BaseModel
from tuuz import Database


class UserModel(BaseModel):
    Table = "ai_user"

    def __init__(self, conn=None):
        super().__init__(conn)

    def api_find_byUsername(self, username):
        return Database.Db(self.db).table(self.Table).where('username', username).find()

    def api_find_byUsernameAndPassword(self, username, password):
        return Database.Db(self.db).table(self.Table).where('username', username).where('password', password).find()

    def api_insert(self, username, password):
        return Database.Db(self.db).table(self.Table).insert({
            'username': username,
            'password': password,
        })

    def api_update(self, username, password):
        return Database.Db(self.db).table(self.Table).where('username', username).update({
            'password': password,
        })
