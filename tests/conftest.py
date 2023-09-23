import asyncio
import pytest

from typing import AsyncGenerator
from alembic.config import Config
from alembic import command
from httpx import AsyncClient
from loguru import logger

from src.main import app
from src.models.users import User
from tests.database import engine_test, async_session_maker, Base, DB_PORT


# 1 вариант создания таблиц
# @pytest.fixture(autouse=True, scope="session")
# TODO Сделать для сессии
@pytest.fixture(autouse=True)
async def init_models():
    """
    Удаление и создание таблиц перед тестом
    """
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


# # Конфиги алембика для инициализации БД
# alembic_cfg = Config("alembic.ini")

# # 2 вариант создания таблиц
# @pytest.fixture(autouse=True)
# async def migrate():
#     """
#     Удаление и создание таблиц перед тестом
#     """
#     await migrate_db()  # Создаем таблицы
#     yield  # Возвращаем БД
#     await downgrage_db()  # Удаляем таблицы
#     await engine_test.dispose()  # Закрываем соединение с БД
#
# async def migrate_db():
#     async with engine_test.begin() as connection:
#         await connection.run_sync(__execute_upgrade)
#
# def __execute_upgrade(connection):
#     alembic_cfg.attributes["connection"] = connection
#     # Применяем последние миграции (создаем таблицы)
#     command.upgrade(alembic_cfg, "head")
#
# async def downgrage_db():
#     async with engine_test.begin() as connection:
#         await connection.run_sync(__execute_downgrage)
#
# def __execute_downgrage(connection):
#     alembic_cfg.attributes["connection"] = connection
#     # Откатываем миграции (удаляем таблицы)
#     command.downgrade(alembic_cfg, "base")

# Пример рекомендуемого кода из документации по асинхронному тестированию FastApi
@pytest.fixture(scope='session')
def event_loop(request):
    """
    Create an instance of the default event loop for each test case.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

# TODO Удалить (не используется)!
# Синхронный клиент (для отправки запросов)
# client = TestClient(app=app)

@pytest.fixture(scope="session")
async def client() -> AsyncGenerator[AsyncClient, None]:
    """
    Асинхронный клиент для выполнения запросов
    """
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

# @pytest.fixture(autouse=True, scope="session")
@pytest.fixture(autouse=True)
async def users():
    """
    Пользователи для тестирования
    """
    async with async_session_maker() as session:
        user_1 = User(username="test-user1", api_key="test-user1")
        user_2 = User(username="test-user2", api_key="test-user2")
        user_3 = User(username="test-user3", api_key="test-user3")

        session.add_all([user_1, user_2, user_3])
        await session.commit()

        yield user_1, user_2, user_3
        # return user_1, user_2, user_3

        # TODO Удалить все записи за раз
        await session.delete(user_1)
        await session.delete(user_2)
        await session.delete(user_3)
        await session.commit()
