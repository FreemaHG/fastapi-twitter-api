from typing import Any, Optional, List

from pydantic import BaseModel, Field, root_validator
from pydantic.utils import GetterDict

# from schemas.base_response import ResponseSchema
# from schemas.image import ImageOutSchema
# from schemas.user import UserSchema
# from schemas.like import LikeSchema
from schemas.base_response import BaseSchema
from schemas.user import BaseUser

class TweetIn(BaseModel):
    tweet_data: str
    tweet_media_ids: Optional[list[int]]

class TweetOut(BaseSchema):
    id: int = Field(alias="tweet_id")

    class Config:
        orm_mode = True
        # Разрешаем псевдонимам изменять названия полей (для ввода и отдачи данных)
        allow_population_by_field_name = True

class Like(BaseModel):
    id: int = Field(alias="user_id")
    username: str = Field(alias="name")

    class Config:
        orm_mode = True
        # Разрешаем псевдонимам изменять названия полей (для ввода и отдачи данных)
        allow_population_by_field_name = True

    @root_validator(pre=True)
    def extract_username(cls, v):
        return vars(v["user"])

class TweetGetter(GetterDict):
    def get(self, key: str, default: Any = None) -> Any:
        if key == "attachments":
            return [
                *[x.path_media for x in self._obj.medias],
            ]
        else:
            return super(TweetGetter, self).get(key, default)

class TweetOutAll(BaseModel):
    id: int
    tweet_data: str = Field(alias="content")
    user: BaseUser = Field(alias="author")
    likes: list[Like]
    attachments: list

    class Config:
        orm_mode = True
        # Разрешаем псевдонимам изменять названия полей (для ввода и отдачи данных)
        allow_population_by_field_name = True
        getter_dict = TweetGetter

class TweetsOut(BaseSchema):
    tweets: list[TweetOutAll]




# TODO Проверить работоспособность своих схем
# class TweetInSchema(BaseModel):
#     """
#     Схема для входных данных при добавлении нового твита
#     """
#     tweet_data: str = Field(max_length=280)
#     tweet_media_ids: Optional[list[int]]
#
# class TweetResponseSchema(ResponseSchema):
#     """
#     Схема для вывода id твита после публикации
#     """
#     tweet_id: int
#
# class TweetOutSchema(BaseModel):
#     """
#     Схема для вывода твита, автора, вложенных изображений и данных по лайкам
#     """
#     id: int
#     body: str = Field(alias="content")
#     images: List[ImageOutSchema]
#     user: UserSchema = Field(alias="author")  # Только поле only=("id", "name")
#     likes: List[LikeSchema]  # Только поле only=("user_id", "user.name")
#
# class TweetListSchema(ResponseSchema):
#     """
#     Схема для вывода списка твитов
#     """
#     tweets: List[TweetOutSchema]
