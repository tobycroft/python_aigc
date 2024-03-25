import json

import config.app as app_conf
from Redis.pyredis import RedisPy


class PubSub:
    def subscribe(self, channel):
        return RedisPy.pubsub().subscribe(app_conf.Project + ":" + channel)

    def publish(self, channel, message):
        return RedisPy.publish(app_conf.Project + ":" + channel, message)

    def publish_struct(self, channel, message_struct):
        message = json.dumps(message_struct)
        return RedisPy.publish(app_conf.Project + ":" + channel, message)
