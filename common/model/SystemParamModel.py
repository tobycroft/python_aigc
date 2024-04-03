from tuuz import Database

Table = 'system_param'


def Api_find(key):
    return Database.Db(self.db).table(Table).where('key', key).find()


def Api_find_value(key):
    return Database.Db(self.db).table(Table).where('key', key).value('value')
