# app/celery_app.py
from celery import Celery
import os
from dotenv import load_dotenv
from app import celeryconfig

load_dotenv()

redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")

celery = Celery(
    "hackernews_tasks",
    broker=redis_url,
    backend=redis_url,
    include=["app.tasks.hn_tasks"]
)

celery.conf.beat_schedule = celeryconfig.beat_schedule

celery.conf.update(
    timezone="UTC",
    enable_utc=True,
)

