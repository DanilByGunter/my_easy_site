"""
Подключение к базе данных для Telegram-бота
"""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from config import config

# Создаем асинхронный движок
engine = create_async_engine(
    config.database_url,
    echo=False,  # Отключаем логирование SQL запросов в продакшене
    pool_pre_ping=True,
    pool_recycle=300,
)

# Создаем фабрику сессий
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncSession:
    """Получить сессию базы данных"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def get_db_session() -> AsyncSession:
    """Получить сессию базы данных для использования в сервисах"""
    return AsyncSessionLocal()
