# CREATE TABLE `ai_team_subtoken` (
#   `id` int NOT NULL,
#   `team_id` int unsigned DEFAULT '0' COMMENT '团队id初期用不上',
#   `type` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '本token调用类型，ollama,openai,fastgpt',
#   `use_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '调用名称',
#   `coin_id` int unsigned DEFAULT '0' COMMENT '扣费模式',
#   `prefix` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '自定义prefix，可以使用team中的团队prefix',
#   `key` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '',
#   `amount` decimal(10,6) DEFAULT '0.000000' COMMENT '积分剩余数量',
#   `change_date` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
#   `date` datetime DEFAULT CURRENT_TIMESTAMP,
#   PRIMARY KEY (`id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
from tuuz import Database

Table = "ai_team_subtoken"


def api_find_byKey(key):
    return Database.Db().table(Table).where("key", key).find()
