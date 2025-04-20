from sqlalchemy import Column, Integer, String, BigInteger
from app.db.database import Base

class Story(Base):
    __tablename__ = "stories"

    id = Column(Integer, primary_key=True, index=True)  # Story ID
    title = Column(String, nullable=False)
    score = Column(Integer)
    url = Column(String)
    author = Column(String, index=True)
    time = Column(BigInteger)
    descendants = Column(Integer)  # Yorum sayısı
    type = Column(String)
