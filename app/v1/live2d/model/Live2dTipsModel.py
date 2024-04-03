# CREATE TABLE `ai_live2d_tips` (
#   `id` int unsigned NOT NULL AUTO_INCREMENT,
#   `team_id` int unsigned DEFAULT '0',
#   `type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '',
#   `selector` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '',
#   `texts` text COLLATE utf8mb4_general_ci,
#   PRIMARY KEY (`id`)
# ) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

from common.BaseModel import BaseModel
from tuuz import Database


class Live2dTipsModel(BaseModel):
    Table = "ai_live2d_tips"

    def __init__(self, conn=None):
        super().__init__(conn)

    def api_select(self):
        return Database.Db(self.db).table(self.Table).select()
