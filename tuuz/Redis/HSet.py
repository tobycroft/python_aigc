import config.app as app_conf
from Redis.pyredis import RedisPy


# 创建 Redis 连接池

def Set(key, field, value):
    return RedisPy.hset(app_conf.Project + ":" + key, field, value)


def Set_map(key, maps):
    return RedisPy.hmset(app_conf.Project + ":" + key, maps)


def Set_struct(key, maps):
    return RedisPy.hmset(app_conf.Project + ":" + key, maps)


def Field_exist(key, field):
    return RedisPy.hexists(app_conf.Project + ":" + key, field)


def Field_incr(key, field, incr_num):
    if isinstance(incr_num, int):
        return RedisPy.hincrby(app_conf.Project + ":" + key, field, incr_num)
    elif isinstance(incr_num, float):
        return RedisPy.hincrbyfloat(app_conf.Project + ":" + key, field, incr_num)


def List_keys(key):
    return RedisPy.hkeys(app_conf.Project + ":" + key)


def List_values(key):
    return RedisPy.hvals(app_conf.Project + ":" + key)


def Get_field(key, field):
    return RedisPy.hget(app_conf.Project + ":" + key, field)


def Count(key):
    return RedisPy.hlen(app_conf.Project + ":" + key)


def Get_all(key):
    return RedisPy.hgetall(app_conf.Project + ":" + key)


def Get_struct(key, model_struct_pointer):
    data = RedisPy.hgetall(app_conf.Project + ":" + key)
    if data:
        for k, v in data.items():
            setattr(model_struct_pointer, k, v)
    return True


def Delete_field(key, field):
    return RedisPy.hdel(app_conf.Project + ":" + key, field)


def Delete(key):
    return RedisPy.delete(key)


def Search(key, cursor, search_pattern, count):
    return RedisPy.hscan(app_conf.Project + ":" + key, cursor, match=search_pattern, count=count)
