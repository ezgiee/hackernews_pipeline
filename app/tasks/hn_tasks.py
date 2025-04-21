import requests
from app.db.database import SessionLocal
from app.models import Story
from app.celery_app import celery
from sqlalchemy.orm import Session

HACKERNEWS_TOP_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

@celery.task
def fetch_top_stories():
    print("🚀 Fetching top stories from Hacker News...")
    db: Session = SessionLocal()

    try:
        response = requests.get(HACKERNEWS_TOP_URL)
        story_ids = response.json()[:100]

        for story_id in story_ids:
            item_response = requests.get(ITEM_URL.format(story_id))
            item = item_response.json()

            if item.get("type") != "story":
                continue

            existing = db.query(Story).filter(Story.id == item["id"]).first()

            if existing:
                # Update if score or descendants changed
                if existing.score != item.get("score") or existing.descendants != item.get("descendants"):
                    existing.score = item.get("score")
                    existing.descendants = item.get("descendants")
                    db.commit()
            else:
                new_story = Story(
                    id=item.get("id"),
                    title=item.get("title"),
                    score=item.get("score"),
                    url=item.get("url"),
                    author=item.get("by"),
                    time=item.get("time"),
                    descendants=item.get("descendants"),
                    type=item.get("type"),
                )
                db.add(new_story)
                db.commit()
    finally:
        db.close()
