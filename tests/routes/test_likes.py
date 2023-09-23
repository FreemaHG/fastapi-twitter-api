from typing import Tuple, Dict

import loguru
import pytest
from http import HTTPStatus

from httpx import AsyncClient

from tests.database import async_session_maker
from src.models.users import User
from src.models.tweets import Tweet
from src.models.tweets import Like


class TestLikes:

    @pytest.fixture
    async def likes(
            self,
            users: Tuple[User],
            tweets: Tuple[Tweet]
    ) -> Tuple[Like, Like]:
        """
        Добавляем записи о лайках
        """
        async with async_session_maker() as session:
            like_1 = Like(user_id=users[0].id, tweets_id=tweets[0].id)
            like_2 = Like(user_id=users[1].id, tweets_id=tweets[1].id)

            session.add_all([like_1, like_2])
            await session.commit()

            yield like_1, like_2
            # return like_1, like_2

            await session.delete(like_1)
            await session.delete(like_2)
            await session.commit()


    async def test_create_like(
            self,
            client: AsyncClient,
            likes: Tuple[Like],
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
            likes: Tuple[Like],
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


    async def test_create_like_locked(
            self,
            client: AsyncClient,
            likes: Tuple[Like],
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
            likes: Tuple[Like],
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
            likes: Tuple[Like],
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


    # FIXME Почему ответ 200 (успешнро удален), вместо 423 - щаблокировано
    # @pytest.mark.skip(reason="Почему-то разрешает удалить твит, вместо того, чтобы запретить. Разобраться!")
    async def test_delete_like_locked(
            self,
            client: AsyncClient,
            likes: Tuple[Like],
            headers: Dict,
            response_locked: Dict
    ) -> None:
        """
        Тестирование вывода ошибки при попытке удалить не существующий лайк
        """
        resp = await client.delete("/tweets/2/likes", headers=headers)
        response_locked["error_message"] = "The user has not yet liked this tweet"

        loguru.logger.info(f"Ответ: {resp.json()}")

        assert resp
        assert resp.status_code == HTTPStatus.LOCKED
        assert resp.json() == response_locked
