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
    """
    Fetch the top stories from Hacker News and trigger background tasks to fetch individual stories.

    This function makes a request to the Hacker News API to get the top story IDs.
    Then, for each story ID, a background task `fetch_and_store_story` is triggered to fetch the full story details.

    Retries the operation in case of failure with exponential backoff (delays: 10, 30, 60 seconds).
    """
    logger.info("Fetching top stories from Hacker News...")
    try:
        # Fetch the top story IDs
        response = requests.get(HACKERNEWS_TOP_URL)
        response.raise_for_status()
        story_ids = response.json()[:101]

        # For each story ID, trigger the fetch_and_store_story task
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
    """
    Fetch an individual story by its ID from Hacker News and store it in the database.

    This function fetches the details of a single story using the provided `story_id`.
    It checks if the story exists and whether all required fields are available before storing it in the database.

    If the story already exists, it updates the score and descendants. If not, it creates a new entry.

    Retries the operation in case of failure with exponential backoff (delays: 10, 30, 60 seconds).
    """
    logger.info(f"Fetching story {story_id}")
    db: Session = SessionLocal()
    try:
        # Fetch the story details
        item_response = requests.get(ITEM_URL.format(story_id))
        item_response.raise_for_status()
        item = item_response.json()

        # Check if the item is a valid story and contains the required fields
        if not item or item.get("type") != "story":
            logger.warning(f"Skipping non-story or empty item: {story_id}")
            return

        required_fields = ["id", "title", "score", "by", "time"]
        if not all(field in item for field in required_fields):
            logger.warning(f"Skipping story {story_id} due to missing fields.")
            return

        # Check if the story already exists in the database
        existing = db.query(Story).filter(Story.id == item["id"]).first()

        if existing:
            # Update existing story if the score or descendants have changed
            if existing.score != item.get("score") or existing.descendants != item.get("descendants"):
                existing.score = item.get("score")
                existing.descendants = item.get("descendants", 0)
                db.commit()
        else:
            # Create a new story entry in the database
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
