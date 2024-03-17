#! /data/python3-venv/bin/python3
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import json
import os

import logging
from loguru import logger

from settings import settings, base_path

broker_url = settings.celery.broker_url
result_backend = settings.celery.broker_url
result_backend_transport_options = {'master_name': "mymaster", 'socket_timeout': 1}
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = "Asia/Shanghai"  # 时区设置
worker_hijack_root_logger = False  # celery默认开启自己的日志，可关闭自定义日志，不关闭自定义日志输出为空
result_expires = 60 * 60 * 24  # 存储结果过期时间（默认1天）
broker_heartbeat = 0
worker_max_tasks_per_child = 5
task_soft_time_limit = 3600
broker_connection_retry_on_startup = True


def formatter(record):
    try:
        from app import get_current_task
    except ImportError:
        task_id = ""
        task_name = ""
    else:
        task = get_current_task()
        if task is None:
            task_id = ""
            task_name = ""
        else:
            task_id = task.request.id
            task_name = task.name

    record["extra"].update(task_id=task_id, task_name=task_name)

    data = {
        "time": record["time"].strftime('%Y-%m-%d %H:%M:%S'),
        "level": record["level"].name,
        "message": record["message"],
        "task_id": task_id,
        "task_name": task_name,
        "function": record["function"]
    }

    record["extra"] = json.dumps(data, default=str, ensure_ascii=False)

    return "{extra}\n"


def init_log():
    time_name = ".{time:YYYY-MM-DD}"
    celery_log = os.path.join(base_path, settings.service.celery_log.celery_path,
                              settings.service.celery_log.celery_name)
    # 初始化log
    print(celery_log)
    logger.add(
        celery_log + time_name,
        level=20,
        rotation="00:00",
        format=formatter
    )


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord):
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        mapper = {
            20: "INFO",
            10: "DEBUG",
            30: "WARNING",
            40: "ERROR",
            50: "CRITICAL"
        }
        logger_opt.log(mapper.get(record.levelno), record.getMessage())
