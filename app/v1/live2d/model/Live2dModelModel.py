# CREATE TABLE `ai_live2d_model` (
#   `id` int unsigned NOT NULL AUTO_INCREMENT,
#   `name` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
#   `modelIntroduce` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
#   `modelPath` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
#   PRIMARY KEY (`id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

from common.BaseModel import BaseModel
from tuuz import Database


class Live2dModelModel(BaseModel):
    Table = "ai_live2d_model"

    def __init__(self, conn=None):
        super().__init__(conn)

    def api_select(self):
        return Database.Db(self.db).table(self.Table).select()
