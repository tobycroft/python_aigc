from redis.asyncio import Redis

import config.app as app_conf
from tuuz.Redis.pyredis import RedisPy


async def Set(key, value, exp=None):
    if exp:
        await Redis(connection_pool=RedisPy).setex(app_conf.Project + ":" + key, int(exp.total_seconds()), value)
    else:
        await Redis(connection_pool=RedisPy).set(name=app_conf.Project + ":" + key, value=value)


async def Get(key):
    return Redis(connection_pool=RedisPy).get(app_conf.Project + ":" + key)


async def Getset(key, value):
    return Redis(connection_pool=RedisPy).getset(app_conf.Project + ":" + key, value)


async def Get_int(key):
    return int(Redis(connection_pool=RedisPy).get(app_conf.Project + ":" + key))


async def Get_int64(key):
    return int(Redis(connection_pool=RedisPy).get(app_conf.Project + ":" + key))


async def Get_float64(key):
    return float(Redis(connection_pool=RedisPy).get(app_conf.Project + ":" + key))


async def Get_bytes(key):
    return Redis(connection_pool=RedisPy).get(app_conf.Project + ":" + key)


async def Get_bool(key):
    return bool(int(Redis(connection_pool=RedisPy).get(app_conf.Project + ":" + key)))


async def Get_time(key):
    return Redis(connection_pool=RedisPy).get(app_conf.Project + ":" + key)


async def Length(key):
    return Redis(connection_pool=RedisPy).strlen(app_conf.Project + ":" + key)


async def Float64_incr(key, incr):
    return Redis(connection_pool=RedisPy).incrbyfloat(app_conf.Project + ":" + key, incr)


async def Int64_incr(key, incr):
    return Redis(connection_pool=RedisPy).incrby(app_conf.Project + ":" + key, incr)


async def Int64_decr(key, decr):
    return Redis(connection_pool=RedisPy).decrby(app_conf.Project + ":" + key, decr)


async def Delete(key):
    return Redis(connection_pool=RedisPy).delete(app_conf.Project + ":" + key)


async def Expire(key, duration):
    return Redis(connection_pool=RedisPy).expire(app_conf.Project + ":" + key, duration)


async def Expire_time(key):
    return Redis(connection_pool=RedisPy).ttl(app_conf.Project + ":" + key)


async def Expire_at(key, expire_at):
    return Redis(connection_pool=RedisPy).expireat(app_conf.Project + ":" + key, expire_at)


async def Check_exists(key):
    return Redis(connection_pool=RedisPy).exists(app_conf.Project + ":" + key)
