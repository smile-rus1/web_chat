#!/bin/sh

echo "⏳ Waiting for database..."

while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
done

echo "✅ Database is ready!"

echo "🚀 Applying migrations..."
alembic upgrade head

echo "🔥 Starting app..."
exec uvicorn src.main:start_app \
  --host 0.0.0.0 \
  --port 8000 \
  --factory
