from http import HTTPStatus

from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from models.users import User
from database import async_session_maker
from services.user import UserService
from utils.exeptions import CustomApiException

class FollowerService:
    """
    Сервис для оформления и удаления подписки между пользователями
    """

    @classmethod
    async def create_follower(cls, current_user: User, following_user_id: int, session: AsyncSession) -> None:
        """
        Создание подписки на пользователя по id
        :param current_user: объект текущего пользователя
        :param following_user_id: id пользователя для подписки
        :return: None
        """
        # async with async_session_maker() as session:

        logger.debug(f"Запрос подписки пользователя id: {current_user.id} на id: {following_user_id} ")

        # Проверка, что текущий пользователь не подписывается сам на себя
        if await UserService.check_user_for_id(current_user_id=current_user.id, user_id=following_user_id):
            logger.error("Попытка подписаться на самого себя")

            raise CustomApiException(
                status_code=HTTPStatus.LOCKED,  # 423 - заблокировано
                detail="You can't subscribe to yourself"
            )

        # Поиск пользователя для подписки
        following_user = await UserService.get_user_for_id(user_id=following_user_id, session=session)

        if not following_user:
            logger.error(f"Не найден пользователь для подписки (id: {following_user_id})")

            raise CustomApiException(
                status_code=HTTPStatus.NOT_FOUND,  # 404
                detail="The subscription user was not found"
            )

        if await cls.check_follower(current_user=current_user, following_user_id=following_user.id):
            logger.warning(f"Подписка уже оформлена")

            raise CustomApiException(
                status_code=HTTPStatus.LOCKED,  # 423
                detail="The user is already subscribed"
            )

        # Получаем текущего пользователя в текущей сессии для записи нового подписчика
        current_user_db = await UserService.get_user_for_id(user_id=current_user.id, session=session)

        current_user_db.following.append(following_user)
        await session.commit()

        logger.info(f"Подписка оформлена")


    @classmethod
    async def check_follower(cls, current_user: User, following_user_id: int) -> bool:
        """
        Проверка наличия подписки
        :param current_user: объект текущего пользователя
        :param following_user_id: id пользователя для подписки
        :return: True - если текущий пользователь уже подписан | False - иначе
        """
        # Проверяем, что текущего пользователя нет в числе подписчиков пользователя на которого он хочет подписаться
        return following_user_id in [following.id for following in current_user.following]


    @classmethod
    async def delete_follower(cls, current_user: User, followed_user_id: int, session: AsyncSession) -> None:
        """
        Удаление подписки на пользователя по id
        :param current_user: объект текущего пользователя
        :param followed_user_id: id пользователя, от которого нужно отписаться
        :return: None
        """
        # 1 - получить текущего пользователя в текущей сессии
        # 2 - проверить и получить пользователя для удаления
        # 3 - проверить, что есть подписка, иначе исключение
        # 4 - удалить подписку
        ...
