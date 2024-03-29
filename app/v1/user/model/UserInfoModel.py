# CREATE TABLE `ai_user_info` (
#   `id` int unsigned NOT NULL AUTO_INCREMENT,
#   `uid` int unsigned DEFAULT '0',
#   `group_name` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
#   `group_img` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
#   `date` datetime DEFAULT CURRENT_TIMESTAMP,
#   PRIMARY KEY (`id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

from common.BaseModel import BaseModel
from tuuz import Database


class UserInfoModel(BaseModel):
    Table = 'ai_user_info'

    def __init__(self, conn=None):
        super().__init__(conn)

    def api_find_byUid(self, uid):
        return Database.Db(self.db).table(self.Table).where('uid', uid).find()

    def api_insert(self, uid, group_name, group_img):
        return Database.Db(self.db).table(self.Table).insert({
            'uid': uid,
            'group_name': group_name,
            'group_img': group_img
        })
