from pydantic import BaseModel
from pydantic import Field

from schemas.base_response import ResponseSchema
# from schemas.base_response import BaseSchema
#
# class MediaOut(BaseSchema):
#     id: int = Field(alias="media_id")
#
#     class Config:
#         orm_mode = True
#         # Разрешаем псевдонимам изменять названия полей (для ввода и отдачи данных)
#         allow_population_by_field_name = True

# TODO Проверить работоспособность своих схем!!!
class ImageResponseSchema(ResponseSchema):
    """
    Схема для вывода id изображения после публикации твита
    """
    id: int = Field(alias="media_id")

    class Config:
        from_attributes = True
        # Разрешаем псевдонимам изменять названия полей (для ввода и отдачи данных)
        populate_by_name = True

        # orm_mode = True
        # allow_population_by_field_name = True


class ImageOutSchema(BaseModel):
    """
    Схема для вывода ссылки на изображения при отображении твитов
    """
    path: str
