# CREATE TABLE `ai_fastgpt_record` (
#   `id` int unsigned NOT NULL AUTO_INCREMENT,
#   `fastgpt_id` int unsigned DEFAULT '0' COMMENT 'fastgpt表的id',
#   `subtoken` varchar(255) COLLATE utf8mb4_general_ci DEFAULT '' COMMENT 'subtoken',
#   `chatId` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '设定的标识符id',
#   `send` json DEFAULT NULL COMMENT '发送的message字段',
#   `reply` json DEFAULT NULL COMMENT '返回的message字段',
#   `completion_tokens` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT 'usage的回复字段',
#   `prompt_tokens` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT 'usuage的提示词字段',
#   `total_tokens` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '算钱用的总和字段',
#   `finish_reason` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT 'stop' COMMENT '完成原因，一般情况甜不甜无所谓的',
#   `amount` decimal(10,6) DEFAULT '0.000000' COMMENT '消耗了多少费用，用coin表的计算值',
#   `change_date` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
#   `date` datetime DEFAULT CURRENT_TIMESTAMP,
#   PRIMARY KEY (`id`)
# ) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
from common.BaseModel import BaseModel
from tuuz import Database


class FastgptRecordModel(BaseModel):
    Table = "ai_fastgpt_record"

    def __init__(self, conn=None):
        super().__init__(conn)

    def api_find_byId(self, id):
        return Database.Db(self.db).table(self.Table).where("id", id).find()

    def api_insert(self, fastgpt_id, subtoken, chatId, send, reply, completion_tokens, prompt_tokens, total_tokens,
                   finish_reason, amount):
        return Database.Db(self.db).table(self.Table).insert({
            "fastgpt_id": fastgpt_id,
            "subtoken": subtoken,
            "chatId": chatId,
            "send": send,
            "reply": reply,
            "completion_tokens": completion_tokens,
            "prompt_tokens": prompt_tokens,
            "total_tokens": total_tokens,
            "finish_reason": finish_reason,
            "amount": amount
        })

    def api_select_byFastgptIdAndChatId(self, fastgpt_id, chatId):
        return Database.Db(self.db).table(self.Table).where("fastgpt_id", fastgpt_id).where("chatId", chatId).order("id asc").select()

    def api_find_byFastgptIdAndChatId(self, fastgpt_id, chatId):
        return Database.Db(self.db).table(self.Table).where("fastgpt_id", fastgpt_id).where("chatId", chatId).order("id desc").find()

    def api_find_bySubtokenIdAndChatId(self, subtoken, chatId):
        return Database.Db(self.db).table(self.Table).where("subtoken", subtoken).where("chatId", chatId).order("id desc").find()
