import os
import pytest

from _pytest._py.path import LocalPath
from http import HTTPStatus
from pathlib import Path
from typing import Dict
from httpx import AsyncClient
from loguru import logger
from sqlalchemy import select

from src.config import ALLOWED_EXTENSIONS
from src.models.images import Image
from tests.database import async_session_maker


_TEST_ROOT_DIR = Path(__file__).resolve().parents[1]  # Корневая директория с тестами


@pytest.mark.image
@pytest.mark.usefixtures("users")
class TestImages:
    @pytest.fixture(scope="class")
    async def good_media_response(self, good_response: Dict):
        """
        Успешный ответ при загрузке изображения к твиту
        """
        good_resp = good_response.copy()
        good_resp["media_id"] = 1

        return good_resp

    @pytest.fixture(scope="class")
    async def bad_media_response(self, bad_response: Dict):
        """
        Неуспешный ответ при загрузке изображения к твиту.
        При загрузке файла неразрешенного формата.
        """
        bad_media_resp = bad_response.copy()
        bad_media_resp["error_type"] = f"{HTTPStatus.UNPROCESSABLE_ENTITY}"
        bad_media_resp["error_message"] = (
            f"The image has an unresolved format. You can only download the "
            f"following formats: {', '.join(ALLOWED_EXTENSIONS)}"
        )

        return bad_media_resp

    @pytest.fixture(scope="class")
    async def image(self):
        image_name = os.path.join(_TEST_ROOT_DIR, "files_for_tests", "test_image.jpg")
        image = open(image_name, "rb")

        return image

    @pytest.fixture(scope="class")
    async def incorrect_file(self):
        file_name = os.path.join(_TEST_ROOT_DIR, "files_for_tests", "test_bad_file.txt")
        file = open(file_name, "rb")

        return file

    async def send_request(self, client: AsyncClient, file):
        """
        Функция для отправки запроса для загрузки файла к твиту
        """
        resp = await client.post(
            "/api/medias", files={"file": file}, headers={"api-key": "test-user1"}
        )

        return resp

    async def get_image(self):
        async with async_session_maker() as session:
            query = select(Image).where(Image.id == 1)
            tweet = await session.execute(query)

            return tweet.scalar_one_or_none()

    async def delete_image(self):
        """
        Функция для удаления файлов при тестировании загрузки изображений
        """
        image = await self.get_image()

        if image:
            _LOCK_PATH = LocalPath()
            _PATH = os.path.join(_LOCK_PATH, "nginx", "static", image.path_media)
            logger.debug(f"Удаление файла: {_PATH}")

            if os.path.isfile(_PATH):
                os.remove(_PATH)

    async def test_load_image(
        self, client: AsyncClient, image, good_media_response: Dict
    ) -> None:
        """
        Тестирование загрузки изображения к твиту
        """
        resp = await self.send_request(client=client, file=image)

        assert resp
        assert resp.status_code == HTTPStatus.CREATED
        assert resp.json() == good_media_response

        await self.delete_image()  # Удаляем созданный файл

    async def test_load_incorrect_file(
        self, client: AsyncClient, incorrect_file, bad_media_response: Dict
    ) -> None:
        """
        Тестирование вывода сообщения об ошибке при попытке загрузить файл неразрешенного формата
        """
        resp = await self.send_request(client=client, file=incorrect_file)

        assert resp
        assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        assert resp.json() == bad_media_response
