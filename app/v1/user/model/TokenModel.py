import Database

Table = 'ai_token'


def Api_insert(uid, token, ip, type=None):
    if Database.Db().table(Table).insert({
        'uid': uid,
        'token': token,
        'ip': ip,
        'type': type
    }) is None:
        return False
    return True
