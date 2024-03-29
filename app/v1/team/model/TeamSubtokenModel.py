# CREATE TABLE `ai_team_subtoken` (
#   `id` int unsigned NOT NULL AUTO_INCREMENT,
#   `uid` int DEFAULT NULL COMMENT '谁创建的',
#   `team_id` int unsigned DEFAULT '0' COMMENT '团队id初期用不上',
#   `coin_id` int DEFAULT NULL COMMENT 'coin表里面找调用类型',
#   `from_id` int DEFAULT NULL COMMENT '不同功能的id，例如来自fastgpt表的id',
#   `prefix` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '自定义prefix，可以使用team中的团队prefix',
#   `key` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT 'aigc',
#   `is_limit` tinyint(1) DEFAULT '1',
#   `amount` decimal(10,6) DEFAULT '0.000000' COMMENT '积分剩余数量',
#   `change_date` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
#   `date` datetime DEFAULT CURRENT_TIMESTAMP,
#   PRIMARY KEY (`id`)
# ) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

from common.BaseModel import BaseModel
from tuuz import Database


class TeamSubtokenModel(BaseModel):
    Table = "ai_team_subtoken"

    def __init__(self, conn=None):
        super().__init__(conn)

    def api_find(self, id):
        return Database.Db(self.db).table(self.Table).where("id", id).find()

    def api_find_byUidAndId(self, uid, id):
        return Database.Db(self.db).table(self.Table).where("uid", uid).where("id", id).find()

    def api_find_byKey(self, key):
        return Database.Db(self.db).table(self.Table).where("key", key).find()

    def api_select_byTeamId(self, team_id):
        return Database.Db(self.db).table(self.Table).where("team_id", team_id).select()

    def api_insert(self, uid, team_id, coin_id, from_id, prefix, key, is_limit, amount):
        return Database.Db(self.db).table(self.Table).insert({
            "uid": uid,
            "team_id": team_id,
            "coin_id": coin_id,
            "from_id": from_id,
            "prefix": prefix,
            "key": key,
            "is_limit": is_limit,
            "amount": amount
        })

    def api_delete(self, team_id, id):
        return Database.Db(self.db).table(self.Table).where("team_id", team_id).where("id", id).delete()

    def api_inc_amount_byKey(self, key, amount):
        return Database.Db(self.db).table(self.Table).where("key", key).setInc("amount", amount)
