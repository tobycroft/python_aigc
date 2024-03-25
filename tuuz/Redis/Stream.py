import config.app as app_conf
from Redis.pyredis import RedisPy


class Stream:
    def __init__(self, stream_channel_name):
        self.stream_channel_name = app_conf.Project + ":" + stream_channel_name

    def Publish(self, value):
        return RedisPy.xadd(self.stream_channel_name, value)

    def XLength(self):
        return RedisPy.xlen(self.stream_channel_name)

    def XRange(self):
        return RedisPy.xrange(self.stream_channel_name, "-", "+")

    def XRevrange(self):
        return RedisPy.xrevrange(self.stream_channel_name, "-", "+")

    def XRead(self):
        return RedisPy.xread({self.stream_channel_name: "0"})

    def XGroup_create_consumer(self, group, consumer):
        return RedisPy.xgroup_create(self.stream_channel_name, group, consumer, mkstream=True)

    def XReadgroup(self, group, consumer):
        return RedisPy.xreadgroup(group, consumer, {self.stream_channel_name: ">"}, count=1)

    @classmethod
    def new(cls, stream_name):
        return cls(stream_name)
