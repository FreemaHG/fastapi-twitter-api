import json
from http import HTTPStatus
from typing import Dict

from httpx import AsyncClient
import pytest


@pytest.mark.tweet
@pytest.mark.usefixtures("users", "tweets")
class TestTweets:
    @pytest.fixture(scope="class")
    async def headers_with_content_type(self, headers: Dict) -> Dict:
        """
        Заголовок при добавлении нового твита
        """
        headers["Content-Type"] = "application/json"
        return headers

    @pytest.fixture(scope="class")
    async def resp_for_new_tweet(self, good_response: Dict) -> Dict:
        """
        Успешный ответ при добавлении нового твита
        """
        good_resp = good_response.copy()
        # id = 4, т.к. фикстурами уже создано 3 твита
        good_resp["tweet_id"] = 4
        return good_resp

    @pytest.fixture(scope="class")
    async def new_tweet(self) -> Dict:
        """
        Данные для добавления нового твита
        """
        return {"tweet_data": "Тестовый твит", "tweet_media_ids": []}

    @pytest.fixture(scope="class")
    async def new_tweet_with_image(self, new_tweet: Dict) -> Dict:
        """
        Данные для добавления нового твита с изображениями
        """
        new_tweet["tweet_media_ids"] = [1, 2]
        return new_tweet

    @pytest.fixture(scope="class")
    async def response_tweet_locked(self, response_locked: Dict) -> Dict:
        response_locked["error_message"] = "The tweet that is being accessed is locked"
        return response_locked

    async def send_request(
        self, client: AsyncClient, headers: Dict, new_tweet_data: Dict = new_tweet
    ):
        """
        Отправка запроса на добавление нового твита
        """
        resp = await client.post(
            "/api/tweets", data=json.dumps(new_tweet_data), headers=headers
        )

        return resp

    async def test_create_tweet(
        self,
        client: AsyncClient,
        new_tweet: Dict,
        headers_with_content_type: Dict,
        resp_for_new_tweet: Dict,
    ) -> None:
        """
        Тестирование добавления твита (без изображений)
        """
        resp = await self.send_request(
            client=client, headers=headers_with_content_type, new_tweet_data=new_tweet
        )

        assert resp
        assert resp.status_code == HTTPStatus.CREATED
        assert resp.json() == resp_for_new_tweet

    async def test_create_tweet_with_images(
        self,
        client: AsyncClient,
        headers_with_content_type: Dict,
        new_tweet_with_image: Dict,
        resp_for_new_tweet: Dict,
    ) -> None:
        """
        Тестирование добавления твита с изображениями
        """
        resp = await self.send_request(
            client=client,
            headers=headers_with_content_type,
            new_tweet_data=new_tweet_with_image,
        )

        # Меняем id для проверки, т.к. текущий твит имеет 4 порядковый номер в БД
        resp_for_new_tweet["tweet_id"] = 5

        assert resp
        assert resp.status_code == HTTPStatus.CREATED
        assert resp.json() == resp_for_new_tweet

    async def test_create_invalid_tweet(
        self,
        client: AsyncClient,
        headers_with_content_type: Dict,
        new_tweet: Dict,
        bad_response: Dict,
    ) -> None:
        """
        Тестирование вывода сообщения об ошибке при публикации слишком длинного твита (> 280 символов)
        """
        new_tweet["tweet_data"] = (
            "Python — идеальный язык для новичка. "
            "Код на Python легко писать и читать, язык стабильно занимает высокие места "
            "в рейтингах популярности, а «питонисты» востребованы почти во всех сферах "
            "IT — программировании, анализе данных, системном администрировании и тестировании. "
            "YouTube, Intel, Pixar, NASA, VK, Яндекс — вот лишь немногие из известных компаний, "
            "которые используют Python в своих продуктах."
        )

        resp = await self.send_request(
            client=client, headers=headers_with_content_type, new_tweet_data=new_tweet
        )

        bad_response["error_type"] = f"{HTTPStatus.UNPROCESSABLE_ENTITY}"
        bad_response["error_message"] = (
            f"The length of the tweet should not exceed 280 characters. "
            f"Current value: {len(new_tweet['tweet_data'])}"
        )

        assert resp
        assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        assert resp.json() == bad_response

    async def test_delete_tweet(
        self, client: AsyncClient, headers: Dict, good_response: Dict
    ) -> None:
        """
        Тестирование удаление твита
        """
        resp = await client.delete("/api/tweets/1", headers=headers)

        assert resp
        assert resp.status_code == HTTPStatus.OK
        assert resp.json() == good_response

    async def test_delete_tweet_not_found(
        self, client: AsyncClient, headers: Dict, response_tweet_not_found: Dict
    ) -> None:
        """
        Тестирование вывода ошибки при попытке удалить несуществующий твит
        """
        resp = await client.delete("/api/tweets/1000", headers=headers)

        assert resp
        assert resp.status_code == HTTPStatus.NOT_FOUND
        assert resp.json() == response_tweet_not_found

    async def test_delete_tweet_locked(
        self, client: AsyncClient, headers: Dict, response_tweet_locked: Dict
    ) -> None:
        """
        Тестирование вывода ошибки при попытке удалить чужой твит
        """
        resp = await client.delete("/api/tweets/2", headers=headers)

        assert resp
        assert resp.status_code == HTTPStatus.LOCKED
        assert resp.json() == response_tweet_locked
