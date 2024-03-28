# CREATE TABLE `ai_user_pack` (
#   `id` int unsigned NOT NULL AUTO_INCREMENT,
#   `uid` int unsigned DEFAULT '0',
#   `pack_id` int DEFAULT '1' COMMENT '用户版本包',
#   `knowledge_base_used` int DEFAULT '0' COMMENT '知识库容量',
#   `ai_point_used` decimal(10,2) DEFAULT NULL COMMENT 'ai积分使用量',
#   `start_date` datetime DEFAULT CURRENT_TIMESTAMP,
#   `end_date` datetime DEFAULT CURRENT_TIMESTAMP,
#   `change_date` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
#   `date` datetime DEFAULT CURRENT_TIMESTAMP,
#   PRIMARY KEY (`id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
from tuuz import Database

Table = 'ai_user_pack'


def api_find_byUid(uid):
    return Database.Db().table(Table).where('uid', uid).find()


def api_insert(uid, pack_id, knowledge_base_used, ai_point_used, start_date, end_date):
    return Database.Db().table(Table).insert(
        {
            'uid': uid,
            'pack_id': pack_id,
            'knowledge_base_used': knowledge_base_used,
            'ai_point_used': ai_point_used,
            'start_date': start_date,
            'end_date': end_date,
        }
    )
