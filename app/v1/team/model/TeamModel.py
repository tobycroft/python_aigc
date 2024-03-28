# CREATE TABLE `ai_team` (
#   `id` int unsigned NOT NULL AUTO_INCREMENT,
#   `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '',
#   `img` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '',
#   `content` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '',
#   `prefix` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT 'aigc' COMMENT '本团队使用的subtoken的开头部分',
#   `change_date` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
#   `date` datetime DEFAULT CURRENT_TIMESTAMP,
#   PRIMARY KEY (`id`)
# ) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

from common.BaseModel import BaseModel
from tuuz import Database


class TeamModel(BaseModel):
    Table = "ai_team"

    def __init__(self, conn=None):
        super().__init__(conn)

    def api_insert(self, uid, name, img, content, prefix):
        return Database.Db(self.db).table(self.Table).insert({
            "uid": uid,
            "name": name,
            "img": img,
            "content": content,
            "prefix": prefix
        })

    def api_insert_uidAndName(self, uid, name):
        return Database.Db(self.db).table(self.Table).insertGetId({
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
