from app.celery_app import celery

@celery.task
def print_hello():
    print("👋 Hello from Celery!")
    return "Task completed"
