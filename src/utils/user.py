from typing import Union, Optional, Dict, Any
from fastapi import Security, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from http import HTTPStatus
from loguru import logger

from services.user import UserService
from database import get_async_session
from utils.exeptions import CustomApiException
from utils.token import TOKEN


# FIXME Попробовать перенести Depends(get_async_session) в services
async def get_current_user(token: str = Security(TOKEN), session: AsyncSession = Depends(get_async_session)):
    """
    Поиск и возврат пользователя из базы данных по токену из header
    """

    if token is None:
        logger.error("Токен не найден в header")

        raise CustomApiException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Valid api-token token is missing"
        )

    current_user = await UserService.get_user_for_key(session=session, token=token)

    if current_user is None:
        raise CustomApiException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Sorry. Wrong api-key token. This user does not exist"
        )

    return current_user
