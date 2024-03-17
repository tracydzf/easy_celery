#! /data/python3-venv/bin/python3
# -*- coding: utf-8 -*-
from __future__ import absolute_import

import logging
import os
import sys


base_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_path)
from celery import Celery
from celery.signals import setup_logging

from celery_config import InterceptHandler, init_log
from celery_statsd import register_celery_events


def create_app():
    app = Celery('celery')

    # 导入celery的配置信息
    app.config_from_object('celery_config')

    app.autodiscover_tasks([
        "tasks.add"
    ])

    register_celery_events()

    return app


app = create_app()


@setup_logging.connect
def setup_logging(*args, **kwargs):
    init_log()
    logging.basicConfig(handlers=[InterceptHandler()], level="INFO")
