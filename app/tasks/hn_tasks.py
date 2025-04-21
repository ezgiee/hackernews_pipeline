import requests
from app.db.database import SessionLocal
from app.models import Story
from app.celery_app import celery
from sqlalchemy.orm import Session
from celery.exceptions import Retry
import logging

HACKERNEWS_TOP_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

RETRY_DELAYS = [10, 30, 60]

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

@celery.task(bind=True, max_retries=3)
def fetch_top_stories(self):
    logger.info("Fetching top stories from Hacker News...")
    try:
        response = requests.get(HACKERNEWS_TOP_URL)
        response.raise_for_status()
        story_ids = response.json()[:101]

        for story_id in story_ids:
            fetch_and_store_story.delay(story_id)
    except Exception as exc:
        try:
            delay_time = RETRY_DELAYS[self.request.retries]
            logger.warning(f"Retrying fetch_top_stories in {delay_time} seconds...")
            raise self.retry(exc=exc, countdown=delay_time)
        except Retry:
            logger.error("Max retries reached for fetch_top_stories")

@celery.task(bind=True, max_retries=3)
def fetch_and_store_story(self, story_id):
    logger.info(f"Fetching story {story_id}")
    db: Session = SessionLocal()
    try:
        item_response = requests.get(ITEM_URL.format(story_id))
        item_response.raise_for_status()
        item = item_response.json()

        if not item or item.get("type") != "story":
            logger.warning(f"Skipping non-story or empty item: {story_id}")
            return

        required_fields = ["id", "title", "score", "by", "time"]
        if not all(field in item for field in required_fields):
            logger.warning(f"Skipping story {story_id} due to missing fields.")
            return

        existing = db.query(Story).filter(Story.id == item["id"]).first()

        if existing:
            if existing.score != item.get("score") or existing.descendants != item.get("descendants"):
                existing.score = item.get("score")
                existing.descendants = item.get("descendants", 0)
                db.commit()
        else:
            new_story = Story(
                id=item["id"],
                title=item.get("title"),
                score=item.get("score"),
                url=item.get("url"),
                author=item.get("by"),
                time=item.get("time"),
                descendants=item.get("descendants", 0),
                type=item.get("type", "story"),
            )
            db.add(new_story)
            db.commit()
    except Exception as exc:
        try:
            delay_time = RETRY_DELAYS[self.request.retries]
            logger.warning(f"Retrying story {story_id} in {delay_time} seconds...")
            raise self.retry(exc=exc, countdown=delay_time)
        except Retry:
            logger.error(f"Max retries reached for story {story_id}")
    finally:
        db.close()
