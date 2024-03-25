import json

import config.app as app_conf
from Redis.pyredis import RedisPy


class PubSub:
    def Subscribe(self, channel):
        return RedisPy.pubsub().subscribe(app_conf.Project + ":" + channel)

    def Publish(self, channel, message):
        return RedisPy.publish(app_conf.Project + ":" + channel, message)

    def Publish_struct(self, channel, message_struct):
        message = json.dumps(message_struct)
        return RedisPy.publish(app_conf.Project + ":" + channel, message)
