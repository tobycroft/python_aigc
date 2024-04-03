# CREATE TABLE `ai_iflytek` (
#   `id` int unsigned NOT NULL AUTO_INCREMENT,
#   `uid` int unsigned DEFAULT '0',
#   `name` varchar(255) COLLATE utf8mb4_general_ci DEFAULT '',
#   `team_id` int unsigned DEFAULT '0',
#   `host` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT 'vms.cn-huadong-1.xf-yun.com',
#   `app_secret` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
#   `app_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
#   `app_key` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
#   `vcn` varchar(255) COLLATE utf8mb4_general_ci DEFAULT '',
#   `change_date` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
#   `date` datetime DEFAULT CURRENT_TIMESTAMP,
#   PRIMARY KEY (`id`)
# ) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

from common.BaseModel import BaseModel
from tuuz import Database


class IflytekModel(BaseModel):
    Table = "ai_iflytek"

    def __init__(self, conn=None):
        super().__init__(conn)

    def api_find_byId(self, id):
        return Database.Db().table(self.Table).where("id", id).find()

    def api_insert(self, uid, name, team_id, host, app_secret, app_id, app_key, vcn):
        return Database.Db().table(self.Table).insert(
            {"uid": uid, "name": name, "team_id": team_id, "host": host, "app_secret": app_secret, "app_id": app_id, "app_key": app_key, "vcn": vcn})

    def api_update_byUidAndId(self, uid, id, name, team_id, host, app_secret, app_id, app_key, vcn):
        return Database.Db().table(self.Table).where("uid", uid).where("id", id).update(
            {"name": name, "team_id": team_id, "host": host, "app_secret": app_secret, "app_id": app_id, "app_key": app_key, "vcn": vcn})

    def api_delete(self, id):
        return Database.Db().table(self.Table).where("id", id).delete()

    def api_delete_byUidAndId(self, uid, id):
        return Database.Db().table(self.Table).where("uid", uid).where("id", id).delete()

    def api_find_byUidAndId(self, uid, id):
        return Database.Db().table(self.Table).where("uid", uid).where("id", id).find()

    def api_select_byUid(self, uid):
        return Database.Db().table(self.Table).where("uid", uid).select()
