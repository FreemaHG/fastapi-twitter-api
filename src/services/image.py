from itertools import chain
from typing import List

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select, ScalarResult
from loguru import logger

from models.images import Image
from utils.image import save_image, delete_images


class ImageService:
    """
    Сервис для сохранения изображений при добавлении нового твита
    """

    @classmethod
    async def save_image(cls, image: UploadFile, session: AsyncSession) -> int:
        """
        Сохранение изображения (без привязки к твиту)
        :param images: файл
        :param session: объект асинхронной сессии
        :param session: объект асинхронной сессии
        :return: id изображения
        """
        logger.debug("Сохранение изображения")

        path = await save_image(file=image)  # Сохранение изображения в файловой системе

        image_obj = Image(path_media=path)  # Создание экземпляра изображения
        session.add(image_obj)  # Добавление изображения в БД
        await session.commit()  # Сохранение в БД

        return image_obj.id


    @classmethod
    async def update_images(cls, tweet_media_ids: List[int], tweet_id: int, session: AsyncSession) -> None:
        """
        Обновление изображений (привязка к твиту)
        :param tweet_media_ids: список с id изображений
        :param tweet_id: id твита для привязки изображений
        :param session: объект асинхронной сессии
        :return: None
        """
        logger.debug(f"Обновление изображений по id: {tweet_media_ids}, tweet_id: {tweet_id}")

        query = update(Image).where(Image.id.in_(tweet_media_ids)).values(tweet_id=tweet_id)
        await session.execute(query)


    @classmethod
    async def get_images(cls, tweet_id: int, session: AsyncSession) -> List[Image]:
        """
        Получить изображения твита.
        Используется при удалении твита для удаления всех его изображений из файловой системы.
        :param tweet_id: id твита
        :param session: объект асинхронной сессии
        :return: None
        """
        logger.debug(f"Поиск изображений твита")

        query = select(Image).filter(Image.tweet_id == tweet_id)
        images = await session.execute(query)

        return list(chain(*images.all()))  # Очищаем результат от вложенных кортежей


    @classmethod
    async def delete_images(cls, tweet_id: int, session: AsyncSession) -> None:
        """
        Удаление изображений твита
        :param tweet_id: id твита
        :param session: объект асинхронной сессии
        :return: None
        """
        logger.debug("Удаление изображений твита")

        images = await cls.get_images(tweet_id=tweet_id, session=session)
        logger.info(f"images: {images}")

        if images:
            await delete_images(images=images)

        else:
            logger.debug("Изображения не найдены")
