from typing import Annotated, Any, Dict
from fastapi import APIRouter, Depends

from schemas.user import UserOutSchema
from schemas.base_response import UnauthorizedResponseSchema
from models.users import User
from utils.user import get_current_user


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
    responses={
        401: {"model": UnauthorizedResponseSchema},
        200: {"model": UserOutSchema}
    },
    status_code=200
)
# TODO Глобальная зависимость - как сделать не указывая Depends!?
async def get_me(current_user: Annotated[User, Depends(get_current_user)]):
    """
    Вывод данных о пользователе: id, username, подписки, подписчики
    """
    return {"user": current_user}
