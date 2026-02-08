#!/bin/bash
set -e

echo "🔄 Starting database initialization..."

# Wait for PostgreSQL to be ready and create database if needed
echo "⏳ Waiting for PostgreSQL to be ready..."
until python -c "
import asyncio
import sys
import os
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

async def setup_database():
    postgres_user = os.getenv('POSTGRES_USER')
    postgres_password = os.getenv('POSTGRES_PASSWORD')
    postgres_db = os.getenv('POSTGRES_DB')

    if not all([postgres_user, postgres_password, postgres_db]):
        print('❌ Missing database environment variables!')
        return False

    # First, try to connect to the target database
    target_url = f'postgresql+asyncpg://{postgres_user}:{postgres_password}@db:5432/{postgres_db}'

    try:
        print(f'🔍 Trying to connect to database: {postgres_db}')
        engine = create_async_engine(target_url)
        async with engine.begin() as conn:
            await conn.execute(text('SELECT 1'))
        await engine.dispose()
        print(f'✅ Database {postgres_db} is ready!')
        return True
    except Exception as e:
        print(f'⚠️  Target database not ready: {e}')

        # Try to connect to postgres database to create our database
        try:
            print('🔧 Trying to create database...')
            postgres_url = f'postgresql+asyncpg://{postgres_user}:{postgres_password}@db:5432/postgres'
            engine = create_async_engine(postgres_url)

            # Check if database exists and create if not
            async with engine.begin() as conn:
                result = await conn.execute(text(f\"SELECT 1 FROM pg_database WHERE datname = '{postgres_db}'\"))
                if not result.fetchone():
                    print(f'📝 Creating database: {postgres_db}')
                    await conn.execute(text(f'CREATE DATABASE {postgres_db}'))
                    print(f'✅ Database {postgres_db} created!')
                else:
                    print(f'ℹ️  Database {postgres_db} already exists')

            await engine.dispose()

            # Now try to connect to our database again
            engine = create_async_engine(target_url)
            async with engine.begin() as conn:
                await conn.execute(text('SELECT 1'))
            await engine.dispose()
            print(f'✅ Successfully connected to {postgres_db}!')
            return True

        except Exception as e2:
            print(f'❌ Failed to setup database: {e2}')
            return False

if not asyncio.run(setup_database()):
    sys.exit(1)
"; do
  echo "💤 Database setup failed, retrying in 3 seconds..."
  sleep 3
done

echo "🗃️  Database is ready! Creating tables and seeding data..."
python seed_db.py

echo "🚀 Starting application..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4