from tuuz import Database

Table = "ai_user"


def Api_find_byUsername(username):
    return Database.Db().table(Table).where('username', username).find()


def Api_insert(username, password):
    return Database.Db().table(Table).insert({
        'username': username,
        'password': password,
    })


def Api_update(username, password):
    return Database.Db().table(Table).where('username', username).update({
        'password': password,
    })
