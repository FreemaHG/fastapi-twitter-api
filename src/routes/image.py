from http import HTTPStatus
from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from src.database import get_async_session
from src.services.image import ImageService
from src.utils.exeptions import CustomApiException
from src.schemas.image import ImageResponseSchema
from src.schemas.base_response import (
    UnauthorizedResponseSchema,
    BadResponseSchema,
    ValidationResponseSchema,
)


router = APIRouter(
    prefix="/api/medias", tags=["medias"]  # URL  # Объединяем URL в группу
)


@router.post(
    "",
    response_model=ImageResponseSchema,
    responses={
        401: {"model": UnauthorizedResponseSchema},
        400: {"model": BadResponseSchema},
        422: {"model": ValidationResponseSchema},
    },
    status_code=201,
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
            detail="The image was not attached to the request",
        )

    # Записываем изображение в файловой системе и создаем запись в БД
    image_id = await ImageService.save_image(image=file, session=session)

    return {"media_id": image_id}
