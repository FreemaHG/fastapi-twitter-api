from typing import Any, Optional, List
from loguru import logger

from pydantic import BaseModel, Field, root_validator, computed_field, validator, field_validator
from pydantic.v1.utils import GetterDict

# from pydantic.utils import GetterDict

from schemas.base_response import ResponseSchema
from schemas.like import LikeSchema
from schemas.user import UserSchema
from schemas.image import ImagePathSchema


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


# class TweetOutGetter(GetterDict):
#     """
#     Класс используется для вывода ссылок изображений без отображения ключа
#     """
#     def get(self, key: str, default: Any = None) -> Any:
#         # if key == "attachments":
#         if key == "attachments":
#             logger.info("Обработка ссылок на изображения")
#             # Проходим циклом по tweet.images и возвращаем значение path_media
#             # Таким образом в качестве ответа в схему в поле значения подставятся строки без ключа
#             # "attachments"[
#             #     path_media_1,
#             #     path_media_2,
#             # ]
#             obj = self._obj
#             logger.info(f"Текущий объект твита: {obj}")
#             logger.info(f"Изображения твита: {obj.images}")
#
#             return [
#                 # *[x.path_media for x in self._obj.images],
#                 *[x.path_media for x in self._obj.images],
#             ]
#
#         else:
#             return super(TweetOutGetter, self).get(key, default)


class TweetOutSchema(BaseModel):
    """
    Схема для вывода твита, автора, вложенных изображений и данных по лайкам
    """
    id: int
    tweet_data: str = Field(alias="content")
    # images: List[ImageOutSchema] = Field(alias="attachments")
    user: UserSchema = Field(alias="author")  # Только поле only=("id", "name")
    # FIXME Не работают!!!
    likes: List[LikeSchema]  # Только поле only=("user_id", "user.name")
    # attachments: List
    # images: List[ImagePathSchema] = Field(alias="attachments")
    images: List[str] = Field(alias="attachments")

    @field_validator('images', mode="before")
    def serialize_images(cls, val: List[ImagePathSchema]):
        """
        Возвращаем список строк с ссылками на изображение
        """
        if isinstance(val, list):
            return [v.path_media for v in val]

        return val

    class Config:
        from_attributes = True
        populate_by_name = True
        # getter_dict = TweetOutGetter

class TweetListSchema(ResponseSchema):
    """
    Схема для вывода списка твитов
    """
    tweets: List[TweetOutSchema]
