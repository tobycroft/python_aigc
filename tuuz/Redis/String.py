import config.app as app_conf
from Redis.pyredis import RedisPy


def Set(key, value, exp=None):
    if exp:
        RedisPy.setex(app_conf.Project + ":" + key, int(exp.total_seconds()), value)
    else:
        RedisPy.set(name=app_conf.Project + ":" + key, value=value)


def Get(key):
    return RedisPy.get(app_conf.Project + ":" + key)


def Getset(key, value):
    return RedisPy.getset(app_conf.Project + ":" + key, value)


def Get_int(key):
    return int(RedisPy.get(app_conf.Project + ":" + key))


def Get_int64(key):
    return int(RedisPy.get(app_conf.Project + ":" + key))


def Get_float64(key):
    return float(RedisPy.get(app_conf.Project + ":" + key))


def Get_bytes(key):
    return RedisPy.get(app_conf.Project + ":" + key)


def Get_bool(key):
    return bool(int(RedisPy.get(app_conf.Project + ":" + key)))


def Get_time(key):
    return RedisPy.get(app_conf.Project + ":" + key)


def Length(key):
    return RedisPy.strlen(app_conf.Project + ":" + key)


def Float64_incr(key, incr):
    return RedisPy.incrbyfloat(app_conf.Project + ":" + key, incr)


def Int64_incr(key, incr):
    return RedisPy.incrby(app_conf.Project + ":" + key, incr)


def Int64_decr(key, decr):
    return RedisPy.decrby(app_conf.Project + ":" + key, decr)


def Delete(key):
    return RedisPy.delete(app_conf.Project + ":" + key)


def Expire(key, duration):
    return RedisPy.expire(app_conf.Project + ":" + key, duration)


def Expire_time(key):
    return RedisPy.ttl(app_conf.Project + ":" + key)


def Expire_at(key, expire_at):
    return RedisPy.expireat(app_conf.Project + ":" + key, expire_at)


def Check_exists(key):
    return RedisPy.exists(app_conf.Project + ":" + key)
