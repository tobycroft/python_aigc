from redis.asyncio import Redis

import config.app as app_conf
from tuuz.Redis.pyredis import RedisPy


class Stream:
    def __init__(self, stream_channel_name):
        self.stream_channel_name = app_conf.Project + ":" + stream_channel_name

    async def Publish(self, value):
        return Redis(connection_pool=RedisPy).xadd(self.stream_channel_name, value)

    async def XLength(self):
        return Redis(connection_pool=RedisPy).xlen(self.stream_channel_name)

    async def XRange(self):
        return Redis(connection_pool=RedisPy).xrange(self.stream_channel_name, "-", "+")

    async def XRevrange(self):
        return Redis(connection_pool=RedisPy).xrevrange(self.stream_channel_name, "-", "+")

    async def XRead(self):
        return Redis(connection_pool=RedisPy).xread({self.stream_channel_name: "0"})

    async def XGroup_create_consumer(self, group, consumer):
        return Redis(connection_pool=RedisPy).xgroup_create(self.stream_channel_name, group, consumer, mkstream=True)

    async def XReadgroup(self, group, consumer):
        return Redis(connection_pool=RedisPy).xreadgroup(group, consumer, {self.stream_channel_name: ">"}, count=1)

    @classmethod
    async def new(cls, stream_name):
        return cls(stream_name)
