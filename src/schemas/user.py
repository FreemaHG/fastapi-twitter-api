from typing import List, Optional
from pydantic import BaseModel

from schemas.base_response import ResponseSchema

class UserSchema(BaseModel):
    """
    Базовая схема для вывода основных данных о пользователе
    """
    id: int
    username: str

    class Config:
        from_attributes = True

class UserDataSchema(UserSchema):
    """
    Схема для вывода детальной информации о пользователе
    """
    following: Optional[List["UserSchema"]] = []
    followers: Optional[List["UserSchema"]] = []

    class Config:
        # Автоматическое преобразование данных ORM-модели в объект схемы для сериализации
        from_attributes = True

class UserOutSchema(ResponseSchema):
    """
    Схема для вывода ответа с детальными данными о пользователе
    """
    user: UserDataSchema
