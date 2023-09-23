import pytest
from httpx import AsyncClient
from http import HTTPStatus

@pytest.mark.token
class TestToken:

    async def test_without_api_key(self, client: AsyncClient) -> None:
        """
        Тестирование вывода ошибки при запросе без api-key в header
        """
        resp = await client.get("/tweets")

        await_response = {
            "result": False,
            "error_type": f"{HTTPStatus.UNAUTHORIZED}",
            "error_message": "User authorization error"
        }

        assert resp.status_code == HTTPStatus.UNAUTHORIZED  # Проверка кода ответа - 401
        assert resp.json() == await_response  # Проверка ответа


    # Используем фикстуру пользователем (создаем пользователя в тестовой БД)
    @pytest.mark.usefixtures("users")
    async def test_unidentified_user(self, client: AsyncClient) -> None:
        """
        Тестирование вывода ошибки при запросе с api-key в header, но без совпадений в БД
        """
        resp = await client.get("/tweets", headers={"api-key": "test-user1000"})

        await_response = {
            "result": False,
            "error_type": f"{HTTPStatus.UNAUTHORIZED}",
            "error_message": "Sorry. Wrong api-key token. This user does not exist"
        }

        assert resp.status_code == HTTPStatus.UNAUTHORIZED
        assert resp.json() == await_response
