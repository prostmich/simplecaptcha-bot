from redis import asyncio as aioredis


class BaseRedis:
    def __init__(
        self,
        connection_uri: str,
        decode_responses: bool = True,
    ):
        self._redis: aioredis.Redis = aioredis.from_url(
            connection_uri, decode_responses=decode_responses
        )

    @property
    def redis(self) -> aioredis.Redis:
        return self._redis
