from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models import Story
from app.auth.jwt_handler import get_current_user
from datetime import datetime

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function to convert UNIX timestamp to a human-readable format
def convert_unix_timestamp_to_human_readable(timestamp: int) -> str:
    """Convert UNIX timestamp to a human-readable date format."""
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

# Endpoint to get a list of stories with filtering, pagination, and sorting
@router.get("/stories")
def get_stories(
    db: Session = Depends(get_db),  # Database session dependency
    current_user: dict = Depends(get_current_user),  # Current authenticated user
    author: str = Query(None),  # Filter stories by author
    min_score: int = Query(None),  # Filter stories by minimum score
    search: str = Query(None),  # Search stories by title
    page: int = Query(1, ge=1),  # Pagination: page number
    limit: int = Query(20, le=100)  # Pagination: limit per page
):
    """
    Get a list of stories based on optional filters (author, score, search) and pagination.

    - **author**: Filter stories by author name (case-insensitive).
    - **min_score**: Filter stories with a score greater than or equal to the given value.
    - **search**: Search stories by title (case-insensitive).
    - **page**: The page number for pagination (defaults to 1).
    - **limit**: The number of stories per page (defaults to 20, maximum 100).

    Returns a paginated list of stories, with each story's timestamp converted to a human-readable format.
    """
    query = db.query(Story)

    if author:
        query = query.filter(Story.author.ilike(f"%{author}%"))
    if min_score:
        query = query.filter(Story.score >= min_score)
    if search:
        query = query.filter(Story.title.ilike(f"%{search}%"))

    total = query.count()

    skip = (page - 1) * limit
    stories = query.offset(skip).limit(limit).all()

    for story in stories:
        story.time = convert_unix_timestamp_to_human_readable(story.time)

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "stories": stories
    }

# Endpoint to get a specific story by its ID
@router.get("/stories/{story_id}")
def get_story(
    story_id: int, 
    db: Session = Depends(get_db),  # Database session dependency
    current_user: dict = Depends(get_current_user)  # Current authenticated user
):
    """
    Get a specific story by its ID.

    - **story_id**: The unique ID of the story.

    Returns the story details with its timestamp converted to a human-readable format, or an error message if not found.
    """
    story = db.query(Story).filter(Story.id == story_id).first()
    if story:
        story.time = convert_unix_timestamp_to_human_readable(story.time)
        return {"story": story}
    else:
        return {"error": "Not found"}
