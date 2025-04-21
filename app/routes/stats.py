from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.database import SessionLocal
from app.models import Story
from app.auth.jwt_handler import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/stats/top-authors")
def top_authors(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    results = (
        db.query(Story.author, func.sum(Story.score).label("total_score"))
        .group_by(Story.author)
        .order_by(func.sum(Story.score).desc())
        .limit(5)
        .all()
    )
    return [{"author": author, "total_score": score} for author, score in results]
