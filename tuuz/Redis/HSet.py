import config.app as app_conf
from Redis.pyredis import RedisPy


# 创建 Redis 连接池

def hash_set(key, field, value):
    return RedisPy.hset(app_conf.Project + ":" + key, field, value)


def hash_set_map(key, maps):
    return RedisPy.hmset(app_conf.Project + ":" + key, maps)


def hash_set_struct(key, maps):
    return RedisPy.hmset(app_conf.Project + ":" + key, maps)


def hash_field_exist(key, field):
    return RedisPy.hexists(app_conf.Project + ":" + key, field)


def hash_field_incr(key, field, incr_num):
    if isinstance(incr_num, int):
        return RedisPy.hincrby(app_conf.Project + ":" + key, field, incr_num)
    elif isinstance(incr_num, float):
        return RedisPy.hincrbyfloat(app_conf.Project + ":" + key, field, incr_num)


def hash_list_keys(key):
    return RedisPy.hkeys(app_conf.Project + ":" + key)


def hash_list_values(key):
    return RedisPy.hvals(app_conf.Project + ":" + key)


def hash_get_field(key, field):
    return RedisPy.hget(app_conf.Project + ":" + key, field)


def hash_count(key):
    return RedisPy.hlen(app_conf.Project + ":" + key)


def hash_get_all(key):
    return RedisPy.hgetall(app_conf.Project + ":" + key)


def hash_get_struct(key, model_struct_pointer):
    data = RedisPy.hgetall(app_conf.Project + ":" + key)
    if data:
        for k, v in data.items():
            setattr(model_struct_pointer, k, v)
    return True


def hash_delete_field(key, field):
    return RedisPy.hdel(app_conf.Project + ":" + key, field)


def hash_delete(key):
    return RedisPy.delete(key)


def hash_search(key, cursor, search_pattern, count):
    return RedisPy.hscan(app_conf.Project + ":" + key, cursor, match=search_pattern, count=count)
