#!/bin/sh

# PostgreSQL veritabanının hazır olup olmadığını kontrol et
echo "⏳ Waiting for PostgreSQL to be ready..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 1
done

case "$ROLE" in
  web)
    echo "🚀 Running DB migration script..."
    python app/init_db.py

    echo "🛠️ Creating test user if not exists..."
    # Test kullanıcısını oluştur
    python -c "
from app.models import User
from app.db.database import SessionLocal
from app.auth.jwt_handler import create_access_token
from sqlalchemy.orm import Session
import bcrypt

# Düz metin şifreyi hashle
def hash_password(password: str):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

db: Session = SessionLocal()
existing_user = db.query(User).filter(User.username == 'admin').first()
if not existing_user:
    test_user = User(
        username='admin',
        password=hash_password('admin')  # Hashlenmiş şifre
    )
    db.add(test_user)
    db.commit()
    print('Test user created!')
else:
    print('Test user already exists.')
db.close()
"

    echo "🌐 Starting FastAPI server..."
    exec uvicorn app.main:app --host 0.0.0.0 --port 8000
    ;;
  worker)
    echo "⚙️ Starting Celery worker..."
    exec celery -A app.celery_app.celery worker --loglevel=info
    ;;
  beat)
    echo "⏰ Starting Celery beat..."
    exec celery -A app.celery_app beat --loglevel=info
    ;;
  *)
    echo "❌ Unknown ROLE: $ROLE"
    exit 1
    ;;
esac
