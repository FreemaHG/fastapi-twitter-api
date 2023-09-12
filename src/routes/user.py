from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from schemas.user import UserOutSchema
from schemas.base_response import (
    UnauthorizedResponseSchema,
    ErrorResponseSchema,
    ValidationResponseSchema,
    ResponseSchema,
    LockedResponseSchema,
)
from models.users import User
from services.user import UserService
from services.follower import FollowerService
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


@router.post(
    "{user_id}/follow",
    # Валидация выходных данных согласно схеме UserOutSchema
    response_model=ResponseSchema,
    # Примеры схем ответов для разных кодов ответов сервера
    responses={
        401: {"model": UnauthorizedResponseSchema},
        404: {"model": ErrorResponseSchema},
        # FIXME Разобраться с проверкой подписки
        422: {"model": ValidationResponseSchema},
        423: {"model": LockedResponseSchema},
    },
    status_code=200
)
async def create_follower(
        user_id: int,
        current_user: Annotated[User, Depends(get_current_user)],
        session: AsyncSession = Depends(get_async_session)
):
    """
    Создание подписки на пользователя по id
    """
    await FollowerService.create_follower(
        current_user=current_user,
        following_user_id=user_id,
        session=session
    )

    return {"result": True}


@router.delete(
    "{user_id}/follow",
    # Валидация выходных данных согласно схеме UserOutSchema
    response_model=ResponseSchema,
    # Примеры схем ответов для разных кодов ответов сервера
    responses={
        401: {"model": UnauthorizedResponseSchema},
        404: {"model": ErrorResponseSchema},
        422: {"model": ValidationResponseSchema},
        423: {"model": LockedResponseSchema},
    },
    status_code=200
)
async def delete_follower(
        user_id: int,
        current_user: Annotated[User, Depends(get_current_user)],
        session: AsyncSession = Depends(get_async_session)
):
    """
    Удаление подписки на пользователя по id
    """
    await FollowerService.delete_follower(
        current_user=current_user,
        followed_user_id=user_id,
        session=session
    )

    return {"result": True}


@router.get(
    "/{user_id}}",
    # Валидация выходных данных согласно схеме UserOutSchema
    response_model=UserOutSchema,
    # Примеры схем ответов для разных кодов ответов сервера
    responses={
        401: {"model": UnauthorizedResponseSchema},
        404: {"model": ErrorResponseSchema},
        422: {"model": ValidationResponseSchema},
        423: {"model": LockedResponseSchema}
    },
    status_code=200
)
async def get_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    """
    Вывод данных о пользователе: id, username, подписки, подписчики
    """
    user = await UserService.get_user_for_id(user_id=user_id, session=session)

    if user is None:
        raise CustomApiException(status_code=404, detail="User not found")

    return {"user": user}
