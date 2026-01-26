import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.database_url:
            # Get from environment variables
            database_url = os.getenv("DATABASE_URL")
            if not database_url:
                # Construct from individual environment variables
                postgres_user = os.getenv("POSTGRES_USER")
                postgres_password = os.getenv("POSTGRES_PASSWORD")
                postgres_db = os.getenv("POSTGRES_DB")

                if not all([postgres_user, postgres_password, postgres_db]):
                    raise ValueError("Database connection parameters not found in environment variables. "
                                     "Please set POSTGRES_USER, POSTGRES_PASSWORD, and POSTGRES_DB.")

                database_url = f"postgresql+asyncpg://{postgres_user}:{postgres_password}@db:5432/{postgres_db}"

            self.database_url = database_url


settings = Settings()
