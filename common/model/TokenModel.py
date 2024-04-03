from tuuz import Database

Table = 'token'


def Api_insert(uid, token, ip, type=None):
    if Database.Db(self.db).table(Table).insert({
        "uid": uid,
        'token': token,
        'ip': ip,
        'type': type
    }) is None:
        return False
    return True


def Api_find_byToken(token):
    return Database.Db(self.db).table(Table).where('token', token).find()


def Api_find_byUidAndToken(uid, token):
    return Database.Db(self.db).table(Table).where("uid", uid).where('token', token).find()
