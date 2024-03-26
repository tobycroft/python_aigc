from tuuz import Database

Table = 'ai_openai'


def Api_find(id):
    return Database.Db().table(Table).where('id', id).find()
