from celery.schedules import crontab

beat_schedule = {
    "fetch-top-stories-every-hour": {
        "task": "app.tasks.hn_tasks.fetch_top_stories",
        "schedule": crontab(minute=15, hour="*"),
    },
}
