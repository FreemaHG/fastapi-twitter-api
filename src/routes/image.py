from typing import Annotated
from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from models.users import User
from schemas.image import ImageResponseSchema
from utils.user import get_current_user
from database import get_async_session


# Роутер для вывода данных о пользователе
router = APIRouter(
    prefix="/medias",  # URL
    tags=["medias"]  # Объединяем URL в группу
)


@router.post("/medias", response_model=ImageResponseSchema, status_code=201)
async def create_upload_file(
    file: UploadFile | None = None,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Загрузка изображения к твиту
    """
    logger.debug("Загрузка изображения к твиту")

    if not file:
        return {"message": "No upload file sent"}
    new_filename = await write_file(file)
    if new_filename:
        new_file = Media(path_media=new_filename)
        session.add(new_file)
        await session.commit()
        return new_file