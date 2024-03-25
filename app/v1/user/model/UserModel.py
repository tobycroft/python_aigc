from tuuz import Database

Table = "ai_user"


def Api_find_byUsername(username):
    return Database.Db().table(Table).where('username', username).find()
