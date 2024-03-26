import configparser

# from redis import ConnectionPool
from redis.asyncio import Redis, ConnectionPool

import config.redis as RedisConfig

cfg = configparser.ConfigParser()
try:
    cfg.read("conf.ini")
except configparser.Error as e:
    print(e)

if "redis" not in cfg:
    cfg["redis"] = {
        "address": "",
        "port": RedisConfig.Redicon_port,
        "username": RedisConfig.Redicon_username,
        "password": RedisConfig.Redicon_password,
        "db": "0"
    }
    with open("conf.ini", "w") as configfile:
        cfg.write(configfile)
    print("redis_ready")
else:
    section = cfg["redis"]
    RedisConfig.Redicon_address = section.get("address", "")
    RedisConfig.Redicon_port = section.get("port", RedisConfig.Redicon_port)
    RedisConfig.Redicon_username = section.get("username", RedisConfig.Redicon_username)
    RedisConfig.Redicon_password = section.get("password", RedisConfig.Redicon_password)
    RedisConfig.Recion_db = int(section.get("db", "0"))

    if RedisConfig.Redicon_address and RedisConfig.Redicon_port:
        RedisConfig.Redicon_on = True
        print("Redis启用并创建连接池……")
        RedisPy = ConnectionPool(host=RedisConfig.Redicon_address,
                                 port=RedisConfig.Redicon_port,
                                 username=RedisConfig.Redicon_username,
                                 password=RedisConfig.Redicon_password,
                                 db=RedisConfig.Recion_db)
        # RedisPy = redis.Redis(host=RedisConfig.Redicon_address,
        #                       port=RedisConfig.Redicon_port,
        #                       username=RedisConfig.Redicon_username,
        #                       password=RedisConfig.Redicon_password,
        #                       db=RedisConfig.Recion_db)


async def init():
    if RedisConfig.Redicon_on:
        rd = Redis(connection_pool=RedisPy)
        print("Redis连接情况：", await rd.ping())
    else:
        print("Redis未启用,Due to", RedisConfig.Redicon_address, RedisConfig.Redicon_port)
