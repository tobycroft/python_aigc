# CREATE TABLE `ai_fastgpt` (
#   `id` int unsigned NOT NULL AUTO_INCREMENT,
#   `uid` int unsigned DEFAULT '0',
#   `name` varchar(255) COLLATE utf8mb4_general_ci DEFAULT '',
#   `key` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '',
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

    def api_insert(self, uid, name, key):
        return Database.Db().table(self.Table).insertGetId({
            "uid": uid,
            "name": name,
            "key": key
        })

    def api_find_byId(self, id):
        return Database.Db().table(self.Table).whereRow("id", id).find()
