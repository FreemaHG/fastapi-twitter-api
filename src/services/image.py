from typing import List

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update
from loguru import logger

from models.images import Image
from utils.image import save_image


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
