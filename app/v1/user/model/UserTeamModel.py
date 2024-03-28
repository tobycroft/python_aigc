# CREATE TABLE `ai_user_team` (
#   `id` int NOT NULL,
#   `uid` int unsigned DEFAULT '0',
#   `team_id` int DEFAULT NULL COMMENT '团队id',
#   `role` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '团队权限',
#   `nickname` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '团队昵称',
#   `change_date` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
#   `date` datetime DEFAULT CURRENT_TIMESTAMP,
#   PRIMARY KEY (`id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

from common.BaseModel import BaseModel
from tuuz import Database


class UserTeamModel(BaseModel):
    Table = "ai_user_team"

    def __init__(self, conn=None):
        super().__init__(conn)

    def api_insert(self, uid, team_id, role, nickname):
        return Database.Db(self.db).table(self.Table).insert({
            "uid": uid,
            "team_id": team_id,
            "role": role,
            "nickname": nickname
        })

    def api_update(self, id, team_id, role, nickname):
        return Database.Db(self.db).table(self.Table).where("id", id).update({
            "team_id": team_id,
            "role": role,
            "nickname": nickname
        })

    def api_delete(self, id):
        return Database.Db(self.db).table(self.Table).where("id", id).delete()

    def api_find(self, id):
        return Database.Db(self.db).table(self.Table).where("id", id).find()

    def api_find_byUidAndTeamId(self, uid, team_id):
        return Database.Db(self.db).table(self.Table).where("uid", uid).where("team_id", team_id).find()

    def api_find_byUidAndTeamIdAndRole(self, uid, team_id, role):
        return Database.Db(self.db).table(self.Table).where("uid", uid).where("team_id", team_id).where("role", role).find()

    def api_select(self, uid):
        return Database.Db(self.db).table(self.Table).where("uid", uid).select()
