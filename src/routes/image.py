from http import HTTPStatus
from typing import Annotated
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from models.users import User
from schemas.image import ImageResponseSchema
from services.image import ImageService
from utils.exeptions import CustomApiException
from utils.user import get_current_user
from database import get_async_session
from schemas.base_response import UnauthorizedResponseSchema, BadResponseSchema, ValidationResponseSchema


# Роутер для вывода данных о пользователе
router = APIRouter(
    prefix="/medias",  # URL
    tags=["medias"]  # Объединяем URL в группу
)


@router.post(
    "",
    response_model=ImageResponseSchema,
    responses={
        401: {"model": UnauthorizedResponseSchema},
        400: {"model": BadResponseSchema},
        422: {"model": ValidationResponseSchema},
    },
    status_code=201
)
async def add_image(
    file: UploadFile,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Загрузка изображения к твиту
    """
    if not file:
        logger.error("Изображение не передано в запросе")

        raise CustomApiException(
            status_code=HTTPStatus.BAD_REQUEST,  # 400
            detail="The image was not attached to the request"
        )

    # Записываем изображение в файловой системе и создаем запись в БД
    image_id = await ImageService.save_image(image=file, session=session)

    return {"media_id": image_id}
