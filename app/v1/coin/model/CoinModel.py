from common.BaseModel import BaseModel
from tuuz import Database


#   `id` int unsigned NOT NULL AUTO_INCREMENT,
#   `type` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '类型，是GPT还是向量模型还是分词模型',
#   `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '引擎名称',
#   `token` decimal(10,0) unsigned DEFAULT '1' COMMENT '一个price可以兑换多少token',
#   `price` decimal(10,2) unsigned DEFAULT '1.00' COMMENT 'CNY全部写1保持1元兑换多少token',
#   `low_in` float unsigned DEFAULT '1' COMMENT '最低一次要买多少token',
#   `max_in` float unsigned DEFAULT '100000' COMMENT '最多一次购买多少token',
#   `change_date` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
#   `date` datetime DEFAULT CURRENT_TIMESTAMP,
#   PRIMARY KEY (`id`)
# ) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='模型';

class CoinModel(BaseModel):
    Table = "ai_coin"

    def __init__(self, conn=None):
        super().__init__(conn)  # CREATE TABLE `ai_coin` (

    def api_find(self, id):
        return Database.Db(self.db).table(self.Table).where('id', id).find()

    def api_find_byName(self, name):
        return Database.Db(self.db).table(self.Table).where('name', name).find()

    def api_select(self):
        return Database.Db(self.db).table(self.Table).select()
