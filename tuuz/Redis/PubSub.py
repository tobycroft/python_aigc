import json

from redis.asyncio import Redis

import config.app as app_conf
from tuuz.Redis.pyredis import RedisPy


class PubSub:
    def Subscribe(self, channel):
        return Redis(connection_pool=RedisPy).pubsub().subscribe(app_conf.Project + ":" + channel)

    def Publish(self, channel, message):
        return Redis(connection_pool=RedisPy).publish(app_conf.Project + ":" + channel, message)

    def Publish_struct(self, channel, message_struct):
        message = json.dumps(message_struct)
        return Redis(connection_pool=RedisPy).publish(app_conf.Project + ":" + channel, message)
