# CREATE TABLE `ai_team_subtoken` (
#   `id` int unsigned NOT NULL AUTO_INCREMENT,
#   `team_id` int unsigned DEFAULT '0' COMMENT '团队id初期用不上',
#   `prefix` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '自定义prefix，可以使用team中的团队prefix',
#   `key` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT 'aigc' COMMENT '密钥',
#   `is_limit` tinyint unsigned DEFAULT '1' COMMENT '是否有扣减积分',
#   `amount` decimal(10,6) DEFAULT '0.000000' COMMENT '积分剩余数量',
#   `change_date` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
#   `date` datetime DEFAULT CURRENT_TIMESTAMP,
#   PRIMARY KEY (`id`)
# ) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

from common.BaseModel import BaseModel
from tuuz import Database


class TeamSubtokenModel(BaseModel):
    Table = "ai_team_subtoken"

    def __init__(self, conn=None):
        super().__init__(conn)

    def api_insert(self, team_id, prefix, key, is_limit, amount):
        return Database.Db(self.db).table(self.Table).insert(
            {"team_id": team_id, "prefix": prefix, "key": key, "is_limit": is_limit, "amount": amount})

    def api_delete(self, team_id, id):
        return Database.Db(self.db).table(self.Table).where("team_id", team_id).where("id", id).delete()

    def api_find_byId(self, id):
        return Database.Db(self.db).table(self.Table).where("id", id).find()

    def api_find_byTeamIdAndKey(self, team_id, key):
        return Database.Db(self.db).table(self.Table).where("team_id", team_id).where("key", key).find()

    def api_update_byId(self, id, amount):
        return Database.Db(self.db).table(self.Table).where("id", id).update({"amount": amount})

    def api_select_inTeamId(self, team_ids):
        return Database.Db(self.db).table(self.Table).whereIn("team_id", team_ids).select()

    def api_find_byIdAndTeamId(self, id, team_id):
        return Database.Db(self.db).table(self.Table).where("id", id).where("team_id", team_id).find()
