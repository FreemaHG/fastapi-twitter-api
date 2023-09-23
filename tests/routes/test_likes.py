from typing import Tuple, Dict

import pytest
from http import HTTPStatus

from httpx import AsyncClient

from tests.database import async_session_maker
from src.models.users import User
from src.models.tweets import Tweet
from src.models.tweets import Like


@pytest.mark.like
# Используем в тестах данные о пользователе и твитах
@pytest.mark.usefixtures("users", "tweets")
class TestLikes:

    @pytest.fixture(scope="class")
    async def likes(
        self,
        users: Tuple[User],
        tweets: Tuple[Tweet]
    ) -> Like:
        """
        Добавляем записи о лайках
        """
        async with async_session_maker() as session:
            like_1 = Like(user_id=users[0].id, tweets_id=tweets[0].id)
            session.add(like_1)
            await session.commit()

            return like_1


    async def test_create_like(
        self,
        client: AsyncClient,
        headers: Dict,
        good_response: Dict,
    ) -> None:
        """
        Тестирование добавления лайка к твиту
        """
        resp = await client.post("/tweets/2/likes", headers=headers)

        assert resp
        assert resp.status_code == HTTPStatus.CREATED
        assert resp.json() == good_response


    async def test_create_like_not_found(
        self,
        client: AsyncClient,
        headers: Dict,
        response_tweet_not_found: Dict,
    ) -> None:
        """
        Тестирование вывода ошибки при попытке поставить лайк несуществующему твиту
        """
        resp = await client.post("/tweets/1000/likes", headers=headers)

        assert resp
        assert resp.status_code == HTTPStatus.NOT_FOUND
        assert resp.json() == response_tweet_not_found

    # Используем фикстуру для создания лайка (будет использоваться во всех следующих тестах к классе!)
    @pytest.mark.usefixtures("likes")
    async def test_create_like_locked(
        self,
        client: AsyncClient,
        headers: Dict,
        response_locked: Dict
    ) -> None:
        """
        Тестирование вывода ошибки при добавлении лайка твиту, у которого уже есть лайк от пользователя
        """
        resp = await client.post("/tweets/1/likes", headers=headers)
        response_locked["error_message"] = "The user has already liked this tweet"

        assert resp
        assert resp.status_code == HTTPStatus.LOCKED
        assert resp.json() == response_locked


    async def test_delete_like(
        self,
        client: AsyncClient,
        headers: Dict,
        good_response: Dict
    ) -> None:
        """
        Тестирование удаления лайка
        """
        resp = await client.delete("/tweets/1/likes", headers=headers)

        assert resp
        assert resp.status_code == HTTPStatus.OK
        assert resp.json() == good_response


    async def test_delete_like_not_found(
        self,
        client: AsyncClient,
        headers: Dict,
        response_tweet_not_found: Dict
    ) -> None:
        """
        Тестирование вывода ошибки при удалении лайка у несуществующей записи
        """
        resp = await client.delete("/tweets/1000/likes", headers=headers)

        assert resp
        assert resp.status_code == HTTPStatus.NOT_FOUND
        assert resp.json() == response_tweet_not_found


    async def test_delete_like_locked(
        self,
        client: AsyncClient,
        headers: Dict,
        response_locked: Dict
    ) -> None:
        """
        Тестирование вывода ошибки при попытке удалить не существующий лайк
        """
        resp = await client.delete("/tweets/3/likes", headers=headers)
        response_locked["error_message"] = "The user has not yet liked this tweet"

        assert resp
        assert resp.status_code == HTTPStatus.LOCKED
        assert resp.json() == response_locked
