from typing import AsyncGenerator
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

from config import DB_USER, DB_PASS, DB_PORT, DB_NAME, DB_HOST


DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Для создания таблиц в декларативном стиле (через модели)
class Base(DeclarativeBase):
    pass

# Объект метадаты передается в таблицы и в него записываются все изменения моделей для того,
# чтобы в дальнейшем можно было применять миграции (либо можно использовать метадату из Base.metadata)
# metadata = MetaData()

# Движок для асинхронного соединения с БД
# echo=True - для вывода SQL-запросов в консоли
# engine = create_async_engine(DATABASE_URL, echo=True)
engine = create_async_engine(DATABASE_URL)

# Сессия для запросов к БД
# FIXME Убрать class_=AsyncSession
# expire_on_commit=False - не делать SQL-запросов к закомиченным объектам
async_session_maker = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# Получение асинхронной сессии
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
