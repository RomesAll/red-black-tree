from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import AsyncGenerator
from app.infrastructure.db.models import BaseOrm

# URL для базы данных
DATABASE_URL = 'sqlite+aiosqlite:///./trees.db'

# Движок SQLAlchemy
engine = create_async_engine(url=DATABASE_URL, echo=False)

# Фабрика сессий
session_factory = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)


async def get_session() -> AsyncGenerator:
    """Асинхронный генератор для получения сессии"""
    try:
        session = session_factory()
        yield session
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()


async def init_db():
    """Создать таблицы в БД"""
    async with engine.begin() as conn:
        await conn.run_sync(BaseOrm.metadata.create_all)