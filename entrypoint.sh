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
