from tuuz import Database

Table = "ai_user"


def api_find_byUsername(username):
    return Database.Db().table(Table).where('username', username).find()


def api_find_byUsernameAndPassword(username, password):
    return Database.Db().table(Table).where('username', username).where('password', password).find()


def api_insert(username, password):
    return Database.Db().table(Table).insert({
        'username': username,
        'password': password,
    })


def api_update(username, password):
    return Database.Db().table(Table).where('username', username).update({
        'password': password,
    })
