from pydantic import BaseModel
from pydantic import Field

from schemas.base_response import ResponseSchema

class ImageResponseSchema(ResponseSchema):
    """
    Схема для вывода id изображения после публикации твита
    """
    id: int = Field(alias="media_id")

    class Config:
        from_attributes = True
        # Использовать псевдоним вместо названия поля
        populate_by_name = True

class ImagePathSchema(BaseModel):
    """
    Схема для вывода ссылки на изображения при отображении твитов
    """
    path_media: str

    class Config:
        from_attributes = True
