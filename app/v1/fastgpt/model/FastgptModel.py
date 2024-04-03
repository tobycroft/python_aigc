# CREATE TABLE `ai_fastgpt` (
#   `id` int unsigned NOT NULL AUTO_INCREMENT,
#   `uid` int unsigned DEFAULT '0' COMMENT '添加人',
#   `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT 'key备注提示',
#   `team_id` int DEFAULT NULL COMMENT 'team_id是添加到哪个队伍里面去的',
#   `key` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '',
#   `base_url` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '访问的url，为空会跑到openai去',
#   `model` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '模型，可以留空',
#   `detail` tinyint(1) DEFAULT '0',
#   `change_date` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
#   `date` datetime DEFAULT CURRENT_TIMESTAMP,
#   PRIMARY KEY (`id`)
# ) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='fastgpt模块';

from common.BaseModel import BaseModel
from tuuz import Database


class FastgptModel(BaseModel):
    Table = "ai_fastgpt"

    def __init__(self, conn=None):
        super().__init__(conn)

    def api_find_byId(self, id):
        return Database.Db().table(self.Table).whereRow("id", id).find()

    def api_select_byUid(self, uid):
        return Database.Db().table(self.Table).whereRow("uid", uid).select()

    def api_update_nameAndKeyAndBaseUrl_byUidAndId(self, uid, id, name, key, base_url):
        return Database.Db().table(self.Table).whereRow("uid", uid).whereRow("id", id).update({"name": name, "key": key, "base_url": base_url})

    def api_delete_byUidAndId(self, uid, id):
        return Database.Db().table(self.Table).whereRow("uid", uid).whereRow("id", id).delete()

    def api_insert(self, uid, name, team_id, key, base_url, model, detail):
        return Database.Db().table(self.Table).insert({"uid": uid, "name": name, "team_id": team_id, "key": key, "base_url": base_url, "model": model, "detail": detail})
