#! /data/python3-venv/bin/python3

import requests
from src.config import settings, statsd


def get_celery_data():
    headers = {
        "Content-Type": "application/json",
    }
    r = requests.get(f"{settings.celery.flower}/workers?json=1", headers=headers)
    if r.status_code != 200:
        return dict(data=[])
    return r.json()


def extract_dashboard_data():
    data = get_celery_data()
    for worker in data["data"]:
        worker_name = worker["hostname"]
        statsd.gauge(f"celery.workers.{worker_name}.active", worker.get("active", 0))
        statsd.gauge(f"celery.workers.{worker_name}.alive", worker.get("worker-online", 0))
        statsd.gauge(f"celery.workers.{worker_name}.processed", worker.get("task-received", 0))
        statsd.gauge(
            f"celery.workers.{worker_name}.processed_succeeded", worker.get("task-succeeded", 0),
        )
        statsd.gauge(
            f"celery.workers.{worker_name}.processed_failed", worker.get("task-failed", 0),
        )
    return