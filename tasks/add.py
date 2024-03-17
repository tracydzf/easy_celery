from app import app
from celery_base_task import CallbackTask
from utils.redis.redis_manager import RedisManager


@app.task(bind=True, base=CallbackTask)
def add_task(self, a, b):
    task_id = self.request.id
    redis: RedisManager = self.redis
    self.loop.run_until_complete(c_add(task_id, redis, a, b))


async def c_add(task_id: str, redis: RedisManager, a, b):
    key = f"add_{a}_{b}"
    await redis.set(key, a + b)
    res = await redis.get((key))
    print(res)
