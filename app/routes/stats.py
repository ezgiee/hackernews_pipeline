from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.database import SessionLocal
from app.models import Story
from app.auth.jwt_handler import get_current_user

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint to get the top authors based on the total score of their stories
@router.get("/stats/top-authors")
def top_authors(
    db: Session = Depends(get_db),  # Database session dependency
    current_user: dict = Depends(get_current_user)  # Current authenticated user
):
    """
    Get the top 5 authors based on the total score of their stories.

    - **current_user**: The user who is making the request (authenticated with JWT token).

    Returns a list of authors with their total score, ordered by total score in descending order.
    """
    results = (
        db.query(Story.author, func.sum(Story.score).label("total_score"))
        .group_by(Story.author)
        .order_by(func.sum(Story.score).desc())
        .limit(5)
        .all()
    )
    return [{"author": author, "total_score": score} for author, score in results]
