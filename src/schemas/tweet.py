from typing import Any, Optional, List

from pydantic import BaseModel, Field, root_validator
from pydantic.utils import GetterDict

from schemas.base_response import ResponseSchema
from schemas.image import ImageOutSchema
from schemas.user import UserSchema
from schemas.like import LikeSchema

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
    tweet_id: int

class TweetOutSchema(BaseModel):
    """
    Схема для вывода твита, автора, вложенных изображений и данных по лайкам
    """
    id: int
    body: str = Field(alias="content")
    images: List[ImageOutSchema]
    user: UserSchema = Field(alias="author")  # Только поле only=("id", "name")
    likes: List[LikeSchema]  # Только поле only=("user_id", "user.name")

class TweetListSchema(ResponseSchema):
    """
    Схема для вывода списка твитов
    """
    tweets: List[TweetOutSchema]
