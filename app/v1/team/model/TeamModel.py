# CREATE TABLE `ai_team` (
#   `id` int unsigned NOT NULL AUTO_INCREMENT,
#   `uid` int unsigned DEFAULT '0' COMMENT '创建者id',
#   `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '',
#   `img` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '',
#   `content` text COLLATE utf8mb4_general_ci,
#   `prefix` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '本团队使用的subtoken的开头部分',
#   `change_date` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
#   `date` datetime DEFAULT CURRENT_TIMESTAMP,
#   PRIMARY KEY (`id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
from pymysql import Connection

from common.BaseModel import BaseModel
from tuuz import Database


class TeamModel(BaseModel):
    Table = "ai_team"

    def __init__(self, Conn: Connection = None):
        super().__init__(Conn)

    def api_insert(self, uid, name, img, content, prefix):
        return Database.Db(self.db).table(self.Table).insert({
            "uid": uid,
            "name": name,
            "img": img,
            "content": content,
            "prefix": prefix
        })

    def api_insert_uidAndName(self, uid, name):
        return Database.Db(self.db).table(self.Table).insert({
            "uid": uid,
            "name": name
        })

    def api_update_byUidAndId(self, uid, id, name, img, content, prefix):
        return Database.Db(self.db).table(self.Table).where("uid", uid).where("id", id).update({
            "name": name,
            "img": img,
            "content": content,
            "prefix": prefix
        })

    def api_select_byUid(self, uid):
        return Database.Db(self.db).table(self.Table).where("uid", uid).select()

    def api_find_byIdAndUid(self, id, uid):
        return Database.Db(self.db).table(self.Table).where("id", id).where("uid", uid).find()

    def api_find_byId(self, id):
        return Database.Db(self.db).table(self.Table).where("id", id).find()

    def api_find_byUidAndName(self, uid, name):
        return Database.Db(self.db).table(self.Table).where("uid", uid).where("name", name).find()

    def api_delete_byUidAndTeamId(self, uid, id):
        return Database.Db(self.db).table(self.Table).where("uid", uid).where("id", id).delete()
