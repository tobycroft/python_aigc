import configparser

import redis

import config.redis

RedisPy = redis.Redis()


def init():
    cfg = configparser.ConfigParser()
    try:
        cfg.read("conf.ini")
    except configparser.Error as e:
        print(e)
        return

    if "redis" not in cfg:
        cfg["redis"] = {
            "address": "",
            "port": config.redis.Redicon_port,
            "username": config.redis.Redicon_username,
            "password": config.redis.Redicon_password,
            "db": "0"
        }
        with open("conf.ini", "w") as configfile:
            cfg.write(configfile)
        print("redis_ready")
    else:
        section = cfg["redis"]
        config.redis.Redicon_address = section.get("address", "")
        config.redis.Redicon_port = section.get("port", config.redis.Redicon_port)
        config.redis.Redicon_username = section.get("username", config.redis.Redicon_username)
        config.redis.Redicon_password = section.get("password", config.redis.Redicon_password)
        config.redis.Recion_db = int(section.get("db", "0"))

        if config.redis.Redicon_address and config.redis.Redicon_port:
            config.redis.Redicon_on = True
    if config.redis.Redicon_on:
        global RedisPy
        RedisPy = redis.Redis(host=config.redis.Redicon_address,
                              port=config.redis.Redicon_port,
                              username=config.redis.Redicon_username,
                              password=config.redis.Redicon_password,
                              db=config.redis.Recion_db)
