import pytest

from typing import Tuple, Dict
from http import HTTPStatus
from sqlalchemy import delete, select
from loguru import logger

from src.models.tweets import Tweet
from src.models.users import User
from tests.database import async_session_maker


# @pytest.fixture(autouse=True, scope="session")
@pytest.fixture(autouse=True)
async def tweets(users: Tuple[User]):
    """
    Твиты для тестирования
    """
    async with async_session_maker() as session:
        tweet_1 = Tweet(tweet_data="Тестовый твит 1", user_id=users[0].id)
        tweet_2 = Tweet(tweet_data="Тестовый твит 2", user_id=users[1].id)

        session.add_all([tweet_1, tweet_2])
        await session.commit()

        # logger.error("Создано 3 твита")

        yield tweet_1, tweet_2
        # return tweet_1, tweet_2

        # TODO Удалить все записи за раз
        await session.delete(tweet_1)
        await session.delete(tweet_2)
        await session.commit()

        # logger.error("Удалено 3 твита")

@pytest.fixture()
async def delete_tweets():

    query = delete(Tweet)

    async with async_session_maker() as session:
        await session.execute(query)
        await session.commit()


# @pytest.fixture()
# async def delete_tweets():
#     async with async_session_maker() as session:
#         query = delete(Tweet)
#         await session.execute(query)
#         await session.commit()


@pytest.fixture()
async def headers():
    """
    Параметр в header для выполнения запросов
    """
    return {"api-key": "test-user1"}


@pytest.fixture()
async def good_response():
    """
    Успешный ответ
    """
    return {"result": True}


@pytest.fixture()
async def bad_response():
    """
    Неуспешный ответ
    """
    return {"result": False}


@pytest.fixture()
async def response_not_found(bad_response: Dict):
    """
    Ответ с кодом 404
    """
    bad_response["error_type"] = f"{HTTPStatus.NOT_FOUND}"

    return bad_response


@pytest.fixture()
async def response_locked(bad_response: Dict):
    """
    Ответ с кодом 423
    """
    bad_response["error_type"] = f"{HTTPStatus.LOCKED}"
    return bad_response


@pytest.fixture()
async def response_tweet_not_found(response_not_found: Dict):
    """
    Ответ с текстом ошибки, что твит не найден
    """
    response_not_found["error_message"] = "Tweet not found"
    return response_not_found
