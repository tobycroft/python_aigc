from common.BaseModel import BaseModel
from tuuz import Database


class IflytekRecordModel(BaseModel):
    Table = "ai_iflytek_record"

    def __init__(self, conn=None):
        super().__init__(conn)

    def api_find_byId(self, id):
        return Database.Db().table(self.Table).where("id", id).find()

    def api_insert(self, fastgpt_id, subtoken_id, chatId, send, reply, completion_tokens, prompt_tokens, total_tokens,
                   finish_reason, amount):
        return Database.Db().table(self.Table).insert({
            "fastgpt_id": fastgpt_id,
            "subtoken_id": subtoken_id,
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
        return Database.Db().table(self.Table).where("fastgpt_id", fastgpt_id).where("chatId", chatId).order("id asc").select()

    def api_find_byFastgptIdAndChatId(self, fastgpt_id, chatId):
        return Database.Db().table(self.Table).where("fastgpt_id", fastgpt_id).where("chatId", chatId).order("id desc").find()

    def api_find_bySubtokenIdAndChatId(self, subtoken_id, chatId):
        return Database.Db().table(self.Table).where("subtoken_id", subtoken_id).where("chatId", chatId).order("id desc").find()
