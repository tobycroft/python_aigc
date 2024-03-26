from redis.asyncio import Redis

import config.app as app_conf
from tuuz.Redis.pyredis import RedisPy


# 创建 Redis 连接池

def Set(key, field, value):
    return Redis(connection_pool=RedisPy).hset(app_conf.Project + ":" + key, field, value)


def Set_map(key, maps):
    return Redis(connection_pool=RedisPy).hmset(app_conf.Project + ":" + key, maps)


def Set_struct(key, maps):
    return Redis(connection_pool=RedisPy).hmset(app_conf.Project + ":" + key, maps)


def Field_exist(key, field):
    return Redis(connection_pool=RedisPy).hexists(app_conf.Project + ":" + key, field)


def Field_incr(key, field, incr_num):
    if isinstance(incr_num, int):
        return Redis(connection_pool=RedisPy).hincrby(app_conf.Project + ":" + key, field, incr_num)
    elif isinstance(incr_num, float):
        return Redis(connection_pool=RedisPy).hincrbyfloat(app_conf.Project + ":" + key, field, incr_num)


def List_keys(key):
    return Redis(connection_pool=RedisPy).hkeys(app_conf.Project + ":" + key)


def List_values(key):
    return Redis(connection_pool=RedisPy).hvals(app_conf.Project + ":" + key)


def Get_field(key, field):
    return Redis(connection_pool=RedisPy).hget(app_conf.Project + ":" + key, field)


def Count(key):
    return Redis(connection_pool=RedisPy).hlen(app_conf.Project + ":" + key)


def Get_all(key):
    return Redis(connection_pool=RedisPy).hgetall(app_conf.Project + ":" + key)


def Get_struct(key, model_struct_pointer):
    data = Redis(connection_pool=RedisPy).hgetall(app_conf.Project + ":" + key)
    if data:
        for k, v in data.items():
            setattr(model_struct_pointer, k, v)
    return True


def Delete_field(key, field):
    return Redis(connection_pool=RedisPy).hdel(app_conf.Project + ":" + key, field)


def Delete(key):
    return Redis(connection_pool=RedisPy).delete(key)


def Search(key, cursor, search_pattern, count):
    return Redis(connection_pool=RedisPy).hscan(app_conf.Project + ":" + key, cursor, match=search_pattern, count=count)
