from sqlalchemy import Column, Integer, String, BigInteger
from app.db.database import Base


class Story(Base):
    __tablename__ = "stories"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    score = Column(Integer)
    url = Column(String)
    author = Column(String, index=True)
    time = Column(BigInteger)
    descendants = Column(Integer)
    type = Column(String)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
