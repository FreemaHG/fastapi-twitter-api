from typing import Optional, List
from pydantic import BaseModel, Field, field_validator, ConfigDict

from src.schemas.base_response import ResponseSchema
from src.schemas.like import LikeSchema
from src.schemas.user import UserSchema
from src.schemas.image import ImagePathSchema


class TweetInSchema(BaseModel):
    """
    Схема для входных данных при добавлении нового твита
    """
    tweet_data: str = Field(max_length=280)
    tweet_media_ids: Optional[list[int]]

class TweetResponseSchema(ResponseSchema):
    """
    Схема для вывода id твита после публикации
    """
    id: int = Field(alias="tweet_id")

    class Config:
        # orm_mode = True
        from_attributes = True
        # Разрешаем псевдонимам изменять названия полей (для ввода и отдачи данных)
        populate_by_name = True

class TweetOutSchema(BaseModel):
    """
    Схема для вывода твита, автора, вложенных изображений и данных по лайкам
    """
    id: int
    tweet_data: str = Field(alias="content")
    user: UserSchema = Field(alias="author")
    likes: List[LikeSchema]
    images: List[str] = Field(alias="attachments")

    @field_validator('images', mode="before")
    def serialize_images(cls, val: List[ImagePathSchema]):
        """
        Возвращаем список строк с ссылками на изображение
        """
        if isinstance(val, list):
            return [v.path_media for v in val]

        return val

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True  # Использовать псевдоним вместо названия поля
    )


class TweetListSchema(ResponseSchema):
    """
    Схема для вывода списка твитов
    """
    tweets: List[TweetOutSchema]
