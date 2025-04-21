from fastapi import FastAPI
from app.routes import stories, stats, auth

app = FastAPI()

app.include_router(auth.router)
app.include_router(stories.router)
app.include_router(stats.router)

@app.get("/")
def read_root():
    return {"message": "HackerNews API is up and running!"}

