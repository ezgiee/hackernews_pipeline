from fastapi import FastAPI
from app.tasks.hn_tasks import print_hello

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "HackerNews API is up and running!"}


@app.get("/run-task")
def run_celery_task():
    task = print_hello.delay()
    return {"task_id": task.id}
