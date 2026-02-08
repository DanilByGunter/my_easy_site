#!/bin/bash
set -e

echo "Waiting for database to be ready..."

# Wait for database to be ready
until python -c "
import asyncio
import sys
from app.settings import settings
from sqlalchemy.ext.asyncio import create_async_engine

async def check_db():
    try:
        engine = create_async_engine(settings.database_url)
        async with engine.begin() as conn:
            await conn.execute('SELECT 1')
        await engine.dispose()
        print('Database is ready!')
        return True
    except Exception as e:
        print(f'Database not ready: {e}')
        return False

if not asyncio.run(check_db()):
    sys.exit(1)
"; do
  echo "Database is unavailable - sleeping"
  sleep 2
done

echo "Database is ready!"

# Run database migrations and seeding
echo "Creating tables and seeding data..."
python seed_db.py

echo "Starting application..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4