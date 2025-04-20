from celery import Celery
import os

redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")

celery = Celery(
    "hackernews_tasks",
    broker=redis_url,
    backend=redis_url
)

celery.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
)
