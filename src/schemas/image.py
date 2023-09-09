from pydantic import BaseModel

from schemas.base_response import ResponseSchema

class ImageResponseSchema(ResponseSchema):
    """
    Схема для вывода id изображения после публикации твита
    """
    media_id: int

class ImageOutSchema(BaseModel):
    """
    Схема для вывода ссылки на изображения при отображении твитов
    """
    path: str
