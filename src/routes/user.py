from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.user import UserOutSchema
from schemas.base_response import UnauthorizedResponseSchema, ErrorResponseSchema, ValidationResponseSchema
from models.users import User
from services.user import UserService
from utils.user import get_current_user
from utils.exeptions import CustomApiException
from database import get_async_session


# Роутер для вывода данных о пользователе
router = APIRouter(
    prefix="/users",  # URL
    tags=["users"]  # Объединяем URL в группу
)


@router.get(
    "/me",
    # Валидация выходных данных согласно схеме UserOutSchema
    response_model=UserOutSchema,
    # Примеры схем ответов для разных кодов ответов сервера
    responses={401: {"model": UnauthorizedResponseSchema}},
    status_code=200
)
async def get_me(current_user: Annotated[User, Depends(get_current_user)]):
    """
    Вывод данных о пользователе: id, username, подписки, подписчики
    """
    return {"user": current_user}


@router.get(
    "/{user_id}}",
    # Валидация выходных данных согласно схеме UserOutSchema
    response_model=UserOutSchema,
    # Примеры схем ответов для разных кодов ответов сервера
    responses={
        401: {"model": UnauthorizedResponseSchema},
        404: {"model": ErrorResponseSchema},
        422: {"model": ValidationResponseSchema}
    },
    status_code=200
)
async def get_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    """
    Вывод данных о пользователе: id, username, подписки, подписчики
    """
    user = await UserService.get_user_for_id(session=session, user_id=user_id)

    if user is None:
        raise CustomApiException(status_code=404, detail="User not found")

    return {"user": user}
