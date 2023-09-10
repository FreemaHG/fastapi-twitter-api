from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from loguru import logger

from models.users import User

class UserService:
    """
    Сервис для вывода данных о пользователе
    """

    @classmethod
    async def get_user_for_key(cls, session: AsyncSession, token: str) -> User | None:
        """
        Возврат объекта пользователя по api-key
        :param token: api-ключ пользователя
        :param session: объект асинхронной сессии
        :return: объект пользователя / False
        """
        logger.debug(f"Поиск пользователя по api-key: {token}")

        query = select(User)\
            .where(User.api_key == token)\
            .options(selectinload(User.following), selectinload(User.followers))
            # selectinload - подгружаем подписчиков (без загрузки нет данных - не проходит валидация схемы)

        result = await session.execute(query)

        return result.scalar_one_or_none()

    @classmethod
    async def get_user_for_id(cls, session: AsyncSession, user_id: int) -> User | None:
        """
        Возврат объекта пользователя по id
        :param user_id: id пользователя
        :param session: объект асинхронной сессии
        :return: объект пользователя / False
        """
        logger.debug(f"Поиск пользователя по id: {user_id}")

        query = select(User)\
            .where(User.id == user_id)\
            .options(selectinload(User.following), selectinload(User.followers))
            # selectinload - подгружаем подписчиков (без загрузки нет данных - не проходит валидация схемы)

        result = await session.execute(query)

        return result.scalar_one_or_none()
