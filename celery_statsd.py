#! /data/python3-venv/bin/python3
# -*- coding: utf-8 -*-
from __future__ import absolute_import
import time

from settings import statsd

_task_start_times = {}


def on_task_published(sender=None, task_id=None, task=None, **kwargs):
    """
    Handle Celery ``after_task_publish`` signals.
    """
    # Increase statsd counter.
    statsd.incr("celery.tasks.%s.published" % kwargs['headers']["task"].split(".")[-1])


def on_task_prerun(sender=None, task_id=None, task=None, **kwargs):
    """
    Handle Celery ``task_prerun``signals.
    """
    # Increase statsd counter.
    # print('celery.%s.start' % task.name)
    statsd.incr("celery.tasks.%s.start" % task.name.split(".")[-1])

    # Keep track of start times. (For logging the duration in the postrun.)
    _task_start_times[task_id] = time.time()


def on_task_postrun(sender=None, task_id=None, task=None, **kwargs):
    """
    Handle Celery ``task_postrun`` signals.
    """
    # Increase statsd counter.
    # print('celery.%s.done' % task.name)
    statsd.incr("celery.tasks.%s.done" % task.name.split(".")[-1])

    # Log duration.
    start_time = _task_start_times.pop(task_id, False)
    if start_time:
        ms = int((time.time() - start_time) * 1000)
        statsd.timing("celery.tasks.%s.runtime" % task.name.split(".")[-1], ms)


def on_task_failure(sender=None, task_id=None, exception=None, *args, **kwargs):
    """
    Handle Celery ``task_failure`` signals.
    """
    # Increase statsd counter.
    # print('celery.%s.failure' % sender.name)
    statsd.incr("celery.tasks.%s.failure" % sender.name.split(".")[-1])


def on_task_success(sender=None, result=None, **kwargs):
    """
    Handle Celery ``task_success`` signals.
    """
    # Increase statsd counter.
    # print('celery.%s.success' % sender.name)
    statsd.incr("celery.tasks.%s.success" % sender.name.split(".")[-1])


def register_celery_events():
    try:
        from app import signals
    except ImportError:
        pass
    else:
        signals.after_task_publish.connect(on_task_published)
        signals.task_prerun.connect(on_task_prerun)
        signals.task_postrun.connect(on_task_postrun)
        signals.task_failure.connect(on_task_failure)
        signals.task_success.connect(on_task_success)
