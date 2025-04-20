import os
from dotenv import load_dotenv

from db.database import Base, engine
from models import Story

def init_db():
    print("📦 Initializing database...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created (or already exist).")

if __name__ == "__main__":
    load_dotenv()
    init_db()
