# CREATE TABLE `ai_qianwen` (
#   `id` int unsigned NOT NULL AUTO_INCREMENT,
#   `uid` int unsigned DEFAULT '0' COMMENT '添加人',
#   `team_id` int DEFAULT NULL COMMENT 'team_id是添加到哪个队伍里面去的',
#   `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT 'key备注提示',
#   `key` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '',
#   `rid` int DEFAULT '0',
#   `model` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '模型，可以留空',
#   PRIMARY KEY (`id`)
# ) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

from common.BaseModel import BaseModel
from tuuz import Database


class FastgptModel(BaseModel):
    Table = "ai_qianwen"

    def __init__(self, conn=None):
        super().__init__(conn)

    def api_insert(self, uid, id, name, key, rid, model):
        return Database.Db().table(self.Table).insert({"uid": uid, "id": id, "name": name, "key": key, "rid": rid, "model": model})

    def api_find_byId(self, id):
        return Database.Db().table(self.Table).where("id", id).find()

    def api_find_byUidAndId(self, uid, id):
        return Database.Db().table(self.Table).where("uid", uid).where("id", id).find()

    def api_select_byUid(self, uid):
        return Database.Db().table(self.Table).where("uid", uid).select()

    def api_update_byUidAndId(self, uid, id, name, key, rid, model):
        return Database.Db().table(self.Table).where("uid", uid).where("id", id).update({"name": name, "key": key, "rid": rid, "model": model})

    def api_delete_byUidAndId(self, uid, id):
        return Database.Db().table(self.Table).where("uid", uid).where("id", id).delete()
