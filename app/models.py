from sqlalchemy import Column, Integer, String, BigInteger
from app.db.database import Base

class Story(Base):
    __tablename__ = "stories"

    title = Column(String, nullable=False)
    score = Column(Integer)
    url = Column(String)
    author = Column(String, index=True)
    time = Column(BigInteger)
    type = Column(String)
