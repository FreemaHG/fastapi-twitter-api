import pytest

from typing import Dict
from http import HTTPStatus
from httpx import AsyncClient


@pytest.mark.follower
@pytest.mark.usefixtures("users")
class TestFollowers:

    @pytest.fixture(scope="class")
    async def response_not_user(
        self,
        response_not_found: Dict
    ):
        """
        Ожидаемый ответ в случае запроса подписки на несуществующего пользователя
        """
        response_not_found["error_message"] = "The subscription user was not found"

        return response_not_found


    @pytest.fixture(scope="class")
    async def response_existing_subscription(
        self,
        response_locked: Dict
    ):
        """
        Ожидаемый ответ в случае запроса подписки на уже подписанного пользователя
        """
        response_locked["error_message"] = "The user is already subscribed"

        return response_locked


    @pytest.fixture(scope="class")
    async def response_subscription_not_found(
        self,
        response_not_found: Dict
    ):
        """
        Ожидаемый ответ в случае отмены подписки от несуществующего пользователя
        """
        response_not_found["error_message"] = "The user to cancel the subscription was not found"

        return response_not_found


    @pytest.fixture(scope="class")
    async def response_among_subscribers(
        self,
        response_locked: Dict
    ):
        """
        Ожидаемый ответ в случае отмены подписки от пользователя, на которого нет подписки
        """
        response_locked["error_message"] = "The user is not among the subscribers"

        return response_locked


    async def test_create_follower(
        self,
        client: AsyncClient,
        headers: Dict,
        good_response: Dict
    ) -> None:
        """
        Тестирование подписки на пользователя
        """
        resp = await client.post("/api/users/3/follow", headers=headers)

        assert resp
        assert resp.status_code == HTTPStatus.CREATED
        assert resp.json() == good_response


    async def test_create_follower_not_found(
            self,
            client: AsyncClient,
            headers: Dict,
            response_not_user: Dict
    ) -> None:
        """
        Тестирование вывода ошибки при попытке подписки на несуществующего пользователя
        """
        resp = await client.post("/api/users/1000/follow", headers=headers)

        assert resp
        assert resp.status_code == HTTPStatus.NOT_FOUND
        assert resp.json() == response_not_user


    async def test_create_follower_locked(
        self,
        client: AsyncClient,
        headers: Dict,
        response_existing_subscription: Dict
    ) -> None:
        """
        Тестирование вывода ошибки при попытке подписки на уже подписанного ранее пользователя
        """
        resp = await client.post("/api/users/2/follow", headers=headers)

        assert resp
        assert resp.status_code == HTTPStatus.LOCKED
        assert resp.json() == response_existing_subscription


    async def test_delete_follower(
        self,
        client: AsyncClient,
        headers: Dict,
        good_response: Dict
    ) -> None:
        """
        Тестирование удаления подписки пользователя
        """
        resp = await client.delete("/api/users/3/follow", headers=headers)

        assert resp
        assert resp.status_code == HTTPStatus.OK
        assert resp.json() == good_response


    async def test_delete_follower_not_found(
        self,
        client: AsyncClient,
        headers: Dict,
        response_subscription_not_found: Dict
    ) -> None:
        """
        Тестирование вывода ошибки при удалении подписки с несуществующего пользователя
        """
        resp = await client.delete("/api/users/1000/follow", headers=headers)

        assert resp
        assert resp.status_code == HTTPStatus.NOT_FOUND
        assert resp.json() == response_subscription_not_found


    async def test_delete_follower_locked(
        self,
        client: AsyncClient,
        headers: Dict,
        response_among_subscribers: Dict
    ) -> None:
        """
        Тестирование вывода ошибки при удалении подписки от пользователя, на которого нет подписки
        """
        resp = await client.delete("/api/users/3/follow", headers=headers)

        assert resp
        assert resp.status_code == HTTPStatus.LOCKED
        assert resp.json() == response_among_subscribers
