from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models import Story
from app.auth.jwt_handler import verify_token

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/stories", dependencies=[Depends(verify_token)])
def get_stories(
    db: Session = Depends(get_db),
    author: str = Query(None),
    min_score: int = Query(None),
    search: str = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(20, le=100)
):
    query = db.query(Story)
    if author:
        query = query.filter(Story.author.ilike(f"%{author}%"))
    if min_score:
        query = query.filter(Story.score >= min_score)
    if search:
        query = query.filter(Story.title.ilike(f"%{search}%"))

    skip = (page - 1) * limit
    stories = query.offset(skip).limit(limit).all()
    return {"stories": stories}

@router.get("/stories/{story_id}", dependencies=[Depends(verify_token)])
def get_story(story_id: int, db: Session = Depends(get_db)):
    story = db.query(Story).filter(Story.id == story_id).first()
    return {"story": story} if story else {"error": "Not found"}
