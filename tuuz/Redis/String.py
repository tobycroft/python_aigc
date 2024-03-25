import config.app as app_conf
from Redis.pyredis import RedisPy


def string_set(key, value, exp=None):
    if exp:
        RedisPy.setex(app_conf.Project + ":" + key, int(exp.total_seconds()), value)
    else:
        RedisPy.set(name=app_conf.Project + ":" + key, value=value)


def string_get(key):
    return RedisPy.get(app_conf.Project + ":" + key)


def string_getset(key, value):
    return RedisPy.getset(app_conf.Project + ":" + key, value)


def string_get_int(key):
    return int(RedisPy.get(app_conf.Project + ":" + key))


def string_get_int64(key):
    return int(RedisPy.get(app_conf.Project + ":" + key))


def string_get_float64(key):
    return float(RedisPy.get(app_conf.Project + ":" + key))


def string_get_bytes(key):
    return RedisPy.get(app_conf.Project + ":" + key)


def string_get_bool(key):
    return bool(int(RedisPy.get(app_conf.Project + ":" + key)))


def string_get_time(key):
    return RedisPy.get(app_conf.Project + ":" + key)


def string_length(key):
    return RedisPy.strlen(app_conf.Project + ":" + key)


def string_float64_incr(key, incr):
    return RedisPy.incrbyfloat(app_conf.Project + ":" + key, incr)


def string_int64_incr(key, incr):
    return RedisPy.incrby(app_conf.Project + ":" + key, incr)


def string_int64_decr(key, decr):
    return RedisPy.decrby(app_conf.Project + ":" + key, decr)


def delete(key):
    return RedisPy.delete(app_conf.Project + ":" + key)


def expire(key, duration):
    return RedisPy.expire(app_conf.Project + ":" + key, duration)


def expire_time(key):
    return RedisPy.ttl(app_conf.Project + ":" + key)


def expire_at(key, expire_at):
    return RedisPy.expireat(app_conf.Project + ":" + key, expire_at)


def check_exists(key):
    return RedisPy.exists(app_conf.Project + ":" + key)
