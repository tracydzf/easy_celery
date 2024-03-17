from aioredis import Redis


class RedisManager:

    def __init__(self, session):
        self.session: Redis = session

    async def close(self):
        await self.session.close()

    async def delete_key(self, key):
        return await self.session.delete(key)

    async def set(self, key, item, expire=None):
        # time to expire should be average time that consumers spend on the session
        result = await self.session.set(key, item, ex=expire)
        return result

    async def get(self, key):
        result = await self.session.get(key)
        return result
