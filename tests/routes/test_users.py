from typing import Dict

import pytest

from httpx import AsyncClient
from http import HTTPStatus

class TestUsers:

    @pytest.fixture(scope="class")
    async def response_data(
            self,
            good_response: Dict
    ) -> Dict:
        """
        Ожидаемый ответ с данными по пользователю
        """
        user_data = {
            "id": 1,
            "name": "test-user1",
            "following": [],
            "followers": [],
        }
        good_response["user"] = user_data

        return good_response

    @pytest.fixture(scope="class")
    async def response_error(
            self,
            bad_response: Dict
    ) -> Dict:
        """
        Ожидаемый ответ в случае запроса не авторизованного пользователя
        """
        bad_response["error_type"] = f"{HTTPStatus.NOT_FOUND}"
        bad_response["error_message"] = "User not found"

        return bad_response

    @pytest.mark.usefixtures("users")
    async def test_user_me_data(
            self,
            client: AsyncClient,
            response_data: Dict,
            headers: Dict,
    ) -> None:
        """
        Тестирование ендпоинта по выводу данных о текущем пользователе
        """
        resp = await client.get("/users/me", headers=headers)

        assert resp
        assert resp.status_code == HTTPStatus.OK
        assert resp.json() == response_data

    @pytest.mark.usefixtures("users")
    async def test_user_data_for_id(
            self,
            client: AsyncClient,
            response_data: Dict,
            headers: Dict
    ) -> None:
        """
        Тестирование ендпоинта по выводу данных о пользователе по переданному id
        """
        resp = await client.get("/users/1", headers=headers)

        assert resp
        assert resp.status_code == HTTPStatus.OK
        assert resp.json() == response_data

    @pytest.mark.usefixtures("users")
    async def test_user_data_for_id_not_found(
            self,
            client: AsyncClient,
            response_error: Dict,
            headers: Dict
    ) -> None:
        """
        Тестирование вывода ошибки при отсутствии пользователя по переданному id
        """
        resp = await client.get("/users/1000", headers=headers)

        assert resp
        assert resp.status_code == HTTPStatus.NOT_FOUND
        assert resp.json() == response_error
