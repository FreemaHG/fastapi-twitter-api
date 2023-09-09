from typing import List
from pydantic import BaseModel, Field

from schemas.base_response import ResponseSchema


class UserSchema(BaseModel):
    """
    Базовая схема пользователя
    """
    id: int
    name: str = Field(max_length=60)
    followers: List["UserSChema"]
    following: List["UserSChema"]

    class Config:
        orm_mode = True

class UserOutSchema(ResponseSchema):
    """
    Схема для вывода данных о пользователе
    """
    user: UserSchema
