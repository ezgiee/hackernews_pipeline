from sqlalchemy import Column, Integer, String, BigInteger
from app.db.database import Base

class Story(Base):
    """
    SQLAlchemy model for storing Hacker News story data.
    """
    __tablename__ = "stories"

    id = Column(Integer, primary_key=True, index=True, doc="Unique story ID from Hacker News")
    title = Column(String, nullable=False, doc="Title of the story")
    score = Column(Integer, doc="Score of the story (upvotes)")
    url = Column(String, doc="URL to the story")
    author = Column(String, index=True, doc="Username of the story author")
    time = Column(BigInteger, doc="UNIX timestamp of when the story was created")
    descendants = Column(Integer, doc="Number of comments (descendants)")
    type = Column(String, doc="Type of the item (usually 'story')")

class User(Base):
    """
    SQLAlchemy model for storing application users.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, doc="Internal user ID")
    username = Column(String, unique=True, index=True, doc="Unique username")
    password = Column(String, doc="Hashed user password")
