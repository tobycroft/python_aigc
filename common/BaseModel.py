from pymysql import Connection

from tuuz import Database


class BaseModel:
    db: Connection = None

    def __init__(self, Conn: Connection = None):
        if Conn is not None:
            self.db = Conn
        else:
            self.db = Database.Db().get_connection()
            pass
