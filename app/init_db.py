import os
from dotenv import load_dotenv
from sqlalchemy import inspect
from app.db.database import Base, engine
from models import Story

def init_db():
    print("📦 Initializing database...")

    inspector = inspect(engine)

    if not inspector.has_table('stories'):
        # Tablo yoksa, oluştur
        Base.metadata.create_all(bind=engine)
        print("✅ Tables created.")
    else:
        print("⚠️ 'stories' table already exists, skipping creation.")

if __name__ == "__main__":
    load_dotenv()
    init_db()
