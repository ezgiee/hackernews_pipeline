#!/bin/sh

echo "⏳ Waiting for PostgreSQL to be ready..."
# DB hazır olana kadar bekle
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 1
done

echo "🚀 Running DB migration script..."
python app/init_db.py

echo "✅ Starting FastAPI server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
