# CREATE TABLE `ai_fastgpt_record` (
#   `id` int unsigned NOT NULL AUTO_INCREMENT,
#   `fastgpt_id` int unsigned DEFAULT '0',
#   `subtoken_id` int unsigned DEFAULT '0',
#   `chatId` varchar(255) COLLATE utf8mb4_general_ci DEFAULT '',
#   `send` json DEFAULT NULL,
#   `reply` json DEFAULT NULL,
#   `completion_tokens` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '',
#   `prompt_tokens` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '',
#   `total_tokens` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '',
#   `finish_reason` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '',
#   `change_date` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
#   `date` datetime DEFAULT CURRENT_TIMESTAMP,
#   PRIMARY KEY (`id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
from tuuz import Database


class FastgptRecordModel:
    Table = "ai_fastgpt_record"

    def __init__(self, conn=None):
        super().__init__(conn)

    def api_find_byId(self, id):
        return Database.Db().table(self.Table).whereRow("id", id).find()

    def api_insert(self, fastgpt_id, subtoken_id, chatId, send, reply, completion_tokens, prompt_tokens, total_tokens):
        return Database.Db().table(self.Table).insert({
            "fastgpt_id": fastgpt_id,
            "subtoken_id": subtoken_id,
            "chatId": chatId,
            "send": send,
            "reply": reply,
            "completion_tokens": completion_tokens,
            "prompt_tokens": prompt_tokens,
            "total_tokens": total_tokens,
        })
