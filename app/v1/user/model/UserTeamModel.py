from tuuz import Database

Table = "ai_user_team"


# CREATE TABLE `ai_user_team` (
#   `id` int NOT NULL,
#   `team_id` int DEFAULT NULL COMMENT '团队id',
#   `role` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '团队权限',
#   `nickname` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '团队昵称',
#   `change_date` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
#   `date` datetime DEFAULT CURRENT_TIMESTAMP,
#   PRIMARY KEY (`id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
def api_insert(team_id, role, nickname):
    return Database.Db().table(Table).insert({
        "team_id": team_id,
        "role": role,
        "nickname": nickname
    })
