# 初始化redis
import asyncio

from settings import settings

# async def init_cluster():
#     """
#     https://github.com/DriverX/aioredis-cluster
#     """
#     startup_nodes = []
#
#     for redis_server in settings.redis.server:
#         startup_nodes.append((redis_server["host"], redis_server["port"]))
#
#     rc = await aioredis_cluster.create_redis_cluster(startup_nodes, password=settings.redis.password,
#                                                      state_reload_interval=60000, encoding='utf-8')
#     return rc


import aioredis.sentinel


async def init_sentinel():
    """
    https://aioredis.readthedocs.io/en/latest/getting-started/#redis-sentinel-client
    """
    redis = aioredis.from_url(settings.celery.broker_url)

    await redis.set("my-key", "value")
    value = await redis.get("my-key")
    print(value)

    return redis


if __name__ == "__main__":
    asyncio.run(init_sentinel())