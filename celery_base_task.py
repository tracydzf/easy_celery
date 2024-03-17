#! /data/python3-venv/bin/python3
# -*- coding: utf-8 -*-
import datetime
import asyncio

import celery
import loguru
from celery import Task

from utils.redis.redis_cluster import init_sentinel
from utils.redis.redis_manager import RedisManager

redis_instance = None


class CallbackTask(Task):
    created_onutc = None

    _event_loop = None

    @property
    def loop(self):
        if self._event_loop is None:
            self._event_loop = asyncio.get_event_loop()
        return self._event_loop

    @property
    def redis(self):
        global redis_instance
        if redis_instance is None:
            redis_sentinels = self.loop.run_until_complete(init_sentinel())
            redis_instance = RedisManager(redis_sentinels)
        return redis_instance

    def on_success(self, retval, task_id, args, kwargs):
        """Success handler.

             Run by the worker if the task executes successfully.

             Arguments:
                 retval (Any): The return value of the task.
                 task_id (str): Unique id of the executed task.
                 args (Tuple): Original arguments for the executed task.
                 kwargs (Dict): Original keyword arguments for the executed task.

             Returns:
                 None: The return value of this handler is ignored.
        """

        success_onutc = datetime.datetime.utcnow()

        loguru.logger.info({
            "msg": "",
            "job_id": task_id,
            "run_time": success_onutc,
            "state": "success",
            "rule_id": task_id,
            "rule_name": celery.current_task.name,
            "insert_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        success_onutc = datetime.datetime.utcnow()

        loguru.logger.error({
            "msg": str(exc),
            "job_id": task_id,
            "run_time": success_onutc,
            "state": "error",
            "rule_id": task_id,
            "rule_name": self.name,
            "insert_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })
