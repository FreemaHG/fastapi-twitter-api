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
    async def get_user_for_key(cls, token: str, session: AsyncSession) -> User | None:
        """
        Возврат объекта пользователя по токену
        :param token: api-ключ пользователя
        :param session: объект асинхронной сессии
        :return: объект пользователя / False
        """
        logger.debug(f"Поиск пользователя по api-key: {token}")

        query = select(User)\
            .where(User.api_key == token)\
            .options(selectinload(User.following), selectinload(User.followers))
            # ВАЖНО: selectinload - подгружаем подписчиков
            # в противном случае по ним нет данных - не проходит валидация схемы!

        result = await session.execute(query)

        return result.scalar_one_or_none()

    @classmethod
    async def get_user_for_id(cls, user_id: int, session: AsyncSession) -> User | None:
        """
        Возврат объекта пользователя по id
        :param user_id: id пользователя
        :param session: объект асинхронной сессии
        :return: объект пользователя / False
        """
        logger.debug(f"Поиск пользователя по id: {user_id}")

        # async with async_session_maker() as session:
        query = select(User)\
            .where(User.id == user_id)\
            .options(selectinload(User.following), selectinload(User.followers))
            # selectinload - подгружаем подписчиков (без загрузки нет данных - не проходит валидация схемы)

        result = await session.execute(query)

        return result.scalar_one_or_none()

    @classmethod
    async def check_user_for_id(cls, current_user_id: int, user_id: int) -> bool:
        """
        Проверка, является ли переданный id текущего пользователя.
        Используется при оформлении подписки пользователя, чтобы проверить, что пользователь не подписался сам на себя.
        :param current_user: объект текущего пользователя
        :param user_id: id пользователя для проверки
        :return: True - если переданный id == current_user.id | False - иначе
        """
        return current_user_id == user_id
