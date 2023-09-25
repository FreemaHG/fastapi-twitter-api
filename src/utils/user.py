from fastapi import Security
from http import HTTPStatus
from loguru import logger

from src.database import async_session_maker
from src.models.users import User
from src.services.user import UserService
from src.utils.exeptions import CustomApiException
from src.utils.token import TOKEN


async def get_current_user(token: str = Security(TOKEN)) -> User | None:
    """
    Поиск и возврат пользователя из базы данных по токену из header
    """

    if token is None:
        logger.error("Токен не найден в header")

        raise CustomApiException(
            status_code=HTTPStatus.UNAUTHORIZED,  # 401
            detail="Valid api-token token is missing",
        )

    async with async_session_maker() as session:
        # Поиск пользователя
        current_user = await UserService.get_user_for_key(token=token, session=session)

        if current_user is None:
            raise CustomApiException(
                status_code=HTTPStatus.UNAUTHORIZED,  # 401
                detail="Sorry. Wrong api-key token. This user does not exist",
            )

        return current_user
