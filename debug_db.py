#!/usr/bin/env python3
import os
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text


async def debug_database():
    print("=== DATABASE DEBUG INFO ===")

    # Print environment variables
    print(f"POSTGRES_USER: {os.getenv('POSTGRES_USER', 'NOT SET')}")
    print(f"POSTGRES_PASSWORD: {os.getenv('POSTGRES_PASSWORD', 'NOT SET')}")
    print(f"POSTGRES_DB: {os.getenv('POSTGRES_DB', 'NOT SET')}")
    print(f"DATABASE_URL: {os.getenv('DATABASE_URL', 'NOT SET')}")

    # Construct database URL
    postgres_user = os.getenv("POSTGRES_USER")
    postgres_password = os.getenv("POSTGRES_PASSWORD")
    postgres_db = os.getenv("POSTGRES_DB")

    if not all([postgres_user, postgres_password, postgres_db]):
        print("ERROR: Missing database environment variables!")
        return

    database_url = f"postgresql+asyncpg://{postgres_user}:{postgres_password}@db:5432/{postgres_db}"
    print(f"Constructed DATABASE_URL: {database_url}")

    # Try to connect
    try:
        print("\n=== TESTING DATABASE CONNECTION ===")
        engine = create_async_engine(database_url, echo=True)

        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT version()"))
            version = result.fetchone()
            print(f"PostgreSQL version: {version[0]}")

            # Check current database
            result = await conn.execute(text("SELECT current_database()"))
            current_db = result.fetchone()
            print(f"Current database: {current_db[0]}")

            # Check current user
            result = await conn.execute(text("SELECT current_user"))
            current_user = result.fetchone()
            print(f"Current user: {current_user[0]}")

            # List databases
            result = await conn.execute(text("SELECT datname FROM pg_database WHERE datistemplate = false"))
            databases = result.fetchall()
            print(f"Available databases: {[db[0] for db in databases]}")

        await engine.dispose()
        print("✅ Database connection successful!")

    except Exception as e:
        print(f"❌ Database connection failed: {e}")

        # Try with postgres database
        try:
            print("\n=== TRYING WITH POSTGRES DATABASE ===")
            fallback_url = f"postgresql+asyncpg://{postgres_user}:{postgres_password}@db:5432/postgres"
            print(f"Fallback URL: {fallback_url}")

            engine = create_async_engine(fallback_url)
            async with engine.begin() as conn:
                result = await conn.execute(text("SELECT current_database()"))
                current_db = result.fetchone()
                print(f"Connected to: {current_db[0]}")

                # Check if our database exists
                result = await conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname = '{postgres_db}'"))
                db_exists = result.fetchone()
                print(f"Database '{postgres_db}' exists: {db_exists is not None}")

                if not db_exists:
                    print(f"Creating database '{postgres_db}'...")
                    await conn.execute(text(f"CREATE DATABASE {postgres_db}"))
                    print("✅ Database created!")

            await engine.dispose()

        except Exception as e2:
            print(f"❌ Fallback connection also failed: {e2}")

if __name__ == "__main__":
    asyncio.run(debug_database())
