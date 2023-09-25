from typing import Annotated
from http import HTTPStatus
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.models.users import User
from src.services.user import UserService
from src.services.follower import FollowerService
from src.utils.user import get_current_user
from src.utils.exeptions import CustomApiException
from src.schemas.user import UserOutSchema
from src.schemas.base_response import (
    UnauthorizedResponseSchema,
    ErrorResponseSchema,
    ValidationResponseSchema,
    ResponseSchema,
    LockedResponseSchema,
)


router = APIRouter(
    prefix="/api/users",  # URL
    tags=["users"]  # Объединяем URL в группу
)


@router.get(
    "/me",
    # Валидация выходных данных согласно схеме UserOutSchema
    response_model=UserOutSchema,
    # Примеры схем ответов для разных кодов ответов сервера
    responses={
        401: {"model": UnauthorizedResponseSchema}
    },
    status_code=200
)
async def get_me(current_user: Annotated[User, Depends(get_current_user)]):
    """
    Вывод данных о текущем пользователе: id, username, подписки, подписчики
    """
    return {"user": current_user}


@router.post(
    "/{user_id}/follow",
    response_model=ResponseSchema,
    responses={
        401: {"model": UnauthorizedResponseSchema},
        404: {"model": ErrorResponseSchema},
        422: {"model": ValidationResponseSchema},
        423: {"model": LockedResponseSchema},
    },
    status_code=201
)
async def create_follower(
    user_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session)
):
    """
    Подписка на пользователя
    """
    await FollowerService.create_follower(
        current_user=current_user,
        following_user_id=user_id,
        session=session
    )

    return {"result": True}


@router.delete(
    "/{user_id}/follow",
    response_model=ResponseSchema,
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
    Отписка от пользователя
    """
    await FollowerService.delete_follower(
        current_user=current_user,
        followed_user_id=user_id,
        session=session
    )

    return {"result": True}


@router.get(
    "/{user_id}",
    response_model=UserOutSchema,
    responses={
        401: {"model": UnauthorizedResponseSchema},
        404: {"model": ErrorResponseSchema},
        422: {"model": ValidationResponseSchema},
        423: {"model": LockedResponseSchema}
    },
    status_code=200
)
async def get_user(
    user_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Вывод данных о пользователе: id, username, подписки, подписчики
    """
    user = await UserService.get_user_for_id(user_id=user_id, session=session)

    if user is None:
        raise CustomApiException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="User not found"
        )

    return {"user": user}
