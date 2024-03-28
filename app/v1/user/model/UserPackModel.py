# CREATE TABLE `ai_user_pack` (
#   `id` int unsigned NOT NULL AUTO_INCREMENT,
#   `uid` int unsigned DEFAULT '0',
#   `pack_id` int DEFAULT '1' COMMENT '用户版本包',
#   `start_date` datetime DEFAULT CURRENT_TIMESTAMP,
#   `end_date` datetime DEFAULT CURRENT_TIMESTAMP,
#   `change_date` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
#   `date` datetime DEFAULT CURRENT_TIMESTAMP,
#   PRIMARY KEY (`id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
from common.BaseModel import BaseModel
from tuuz import Database


class UserPackModel(BaseModel):
    Table = "ai_user_pack"

    def __init__(self, conn=None):
        super().__init__(conn)

    def api_find_byUid(self, uid):
        return Database.Db(self.db).table(self.Table).where('uid', uid).find()

    def api_insert(self, uid, pack_id, start_date, end_date):
        return Database.Db(self.db).table(self.Table).insert(
            {
                'uid': uid,
                'pack_id': pack_id,
                'start_date': start_date,
                'end_date': end_date,
            }
        )
